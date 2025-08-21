"""
알림 태스크
"""
import logging
from decimal import Decimal
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from catalog.models import Watch, Product, Offer
from catalog.providers.mock import MockProvider
from catalog.services.matching import ProductMatcher

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='alerts.scan_watches')
def scan_watches(self):
    """활성 Watch 스캔 및 알림 전송"""
    logger.info("Watch 스캔 시작")
    
    try:
        # 활성 Watch 조회
        active_watches = Watch.objects.filter(is_active=True).select_related('product')
        
        if not active_watches.exists():
            logger.info("활성 Watch가 없습니다.")
            return
        
        logger.info(f"활성 Watch {active_watches.count()}개 발견")
        
        # Mock 프로바이더로 최신 오퍼 갱신
        mock_provider = MockProvider()
        matcher = ProductMatcher()
        
        for watch in active_watches:
            try:
                # 상품 관련 오퍼 갱신
                update_product_offers(watch.product, mock_provider)
                
                # 가격 체크 및 알림
                check_price_and_alert(watch)
                
            except Exception as e:
                logger.error(f"Watch {watch.id} 처리 중 오류: {str(e)}")
                continue
        
        logger.info("Watch 스캔 완료")
        
    except Exception as e:
        logger.error(f"Watch 스캔 중 오류: {str(e)}")
        raise


def update_product_offers(product: Product, provider):
    """상품의 최신 오퍼 갱신"""
    try:
        # 상품명으로 검색하여 최신 오퍼 가져오기
        # 동기 방식으로 변경 (Celery 태스크는 동기 함수여야 함)
        import asyncio
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            search_result = loop.run_until_complete(provider.search(product.name))
        finally:
            loop.close()
        
        if not search_result.offers:
            logger.info(f"상품 {product.id}에 대한 오퍼를 찾을 수 없습니다.")
            return
        
        # 기존 오퍼와 비교하여 새로운 오퍼만 추가
        existing_urls = set(Offer.objects.filter(product=product).values_list('url', flat=True))
        
        for offer_like in search_result.offers:
            if offer_like.url not in existing_urls:
                # 새 오퍼 생성
                offer = Offer.objects.create(
                    product=product,
                    marketplace=offer_like.marketplace,
                    seller=offer_like.seller,
                    price=offer_like.price,
                    shipping_fee=offer_like.shipping_fee,
                    url=offer_like.url,
                    affiliate_url=offer_like.affiliate_url,
                    fetched_at=timezone.now()
                )
                
                # 가격 히스토리 기록
                from catalog.models import PriceHistory
                PriceHistory.objects.create(
                    offer=offer,
                    price=offer.price,
                    total_price=offer.total_price,
                    recorded_at=timezone.now()
                )
                
                logger.info(f"새 오퍼 생성: {offer.marketplace} - {offer.price}원")
        
    except Exception as e:
        logger.error(f"상품 {product.id} 오퍼 갱신 중 오류: {str(e)}")


def check_price_and_alert(watch: Watch):
    """가격 체크 및 알림 전송"""
    try:
        # 상품의 최신 오퍼 조회
        latest_offers = Offer.objects.filter(
            product=watch.product
        ).order_by('-fetched_at')[:5]
        
        if not latest_offers.exists():
            logger.info(f"Watch {watch.id}에 대한 최신 오퍼가 없습니다.")
            return
        
        # 최저가 찾기
        best_offer = min(latest_offers, key=lambda x: x.total_price)
        best_total_price = best_offer.total_price
        
        # 목표가 이하인지 확인
        if best_total_price <= watch.target_price:
            logger.info(f"Watch {watch.id} 목표가 달성: {best_total_price}원 <= {watch.target_price}원")
            
            # 알림 전송
            send_price_alert(watch, best_offer, best_total_price)
            
            # Watch 비활성화 (선택사항)
            # watch.is_active = False
            # watch.save()
            
        else:
            logger.debug(f"Watch {watch.id} 목표가 미달성: {best_total_price}원 > {watch.target_price}원")
    
    except Exception as e:
        logger.error(f"Watch {watch.id} 가격 체크 중 오류: {str(e)}")


def send_price_alert(watch: Watch, offer: Offer, current_price: Decimal):
    """가격 알림 전송"""
    try:
        subject = f"🎯 가격 알림: {watch.product.display_name}"
        
        message = f"""
가격 모니터링 알림

상품: {watch.product.display_name}
목표가: {watch.target_price:,}원
현재 최저가: {current_price:,}원
마켓플레이스: {offer.marketplace}
판매자: {offer.seller}
상품 URL: {offer.url}

목표가에 도달했습니다! 🎉
        """.strip()
        
        # 개발 환경에서는 콘솔/파일 출력으로 대체
        if settings.DEBUG:
            logger.info(f"=== 가격 알림 ===\n{subject}\n{message}")
            
            # 파일에도 기록
            import os
            from pathlib import Path
            
            log_dir = Path(settings.BASE_DIR) / 'logs'
            log_dir.mkdir(exist_ok=True)
            
            alert_log_file = log_dir / 'price_alerts.log'
            with open(alert_log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timezone.now()}] {subject}\n{message}\n{'='*50}\n")
        
        else:
            # 프로덕션 환경에서는 이메일 전송
            # 실제 구현 시 사용자 이메일 주소 필요
            user_email = f"user_{watch.user_id}@example.com"  # 임시
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )
            
            logger.info(f"가격 알림 이메일 전송 완료: {user_email}")
    
    except Exception as e:
        logger.error(f"가격 알림 전송 중 오류: {str(e)}")


@shared_task(bind=True, name='alerts.scan_single_watch')
def scan_single_watch(self, watch_id: int):
    """단일 Watch 스캔 (즉시 스캔용)"""
    try:
        watch = Watch.objects.get(id=watch_id, is_active=True)
        logger.info(f"단일 Watch {watch_id} 스캔 시작")
        
        # Mock 프로바이더로 오퍼 갱신
        mock_provider = MockProvider()
        update_product_offers(watch.product, mock_provider)
        
        # 가격 체크 및 알림
        check_price_and_alert(watch)
        
        logger.info(f"단일 Watch {watch_id} 스캔 완료")
        
    except Watch.DoesNotExist:
        logger.warning(f"Watch {watch_id}를 찾을 수 없습니다.")
    except Exception as e:
        logger.error(f"단일 Watch {watch_id} 스캔 중 오류: {str(e)}")


@shared_task(bind=True, name='alerts.test_alert')
def test_alert(self):
    """알림 시스템 테스트 태스크"""
    logger.info("알림 시스템 테스트 시작")
    
    try:
        # 테스트 알림 전송
        test_watch = Watch.objects.filter(is_active=True).first()
        
        if test_watch:
            test_offer = Offer.objects.filter(product=test_watch.product).first()
            
            if test_offer:
                send_price_alert(
                    test_watch, 
                    test_offer, 
                    test_watch.target_price - Decimal("10000")  # 목표가보다 낮은 가격
                )
                logger.info("테스트 알림 전송 완료")
            else:
                logger.warning("테스트용 오퍼가 없습니다.")
        else:
            logger.warning("테스트용 Watch가 없습니다.")
    
    except Exception as e:
        logger.error(f"테스트 알림 중 오류: {str(e)}")
    
    logger.info("알림 시스템 테스트 완료")
