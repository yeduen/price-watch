"""
Celery configuration
"""
import os
from celery import Celery
from celery.schedules import crontab

# Django 설정 모듈 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketwatch.settings')

# Celery 앱 생성
app = Celery('marketwatch')

# Django 설정에서 Celery 설정 로드
app.config_from_object('django.conf:settings', namespace='CELERY')

# 태스크 자동 발견
app.autodiscover_tasks()

# Beat 스케줄 설정
app.conf.beat_schedule = {
    # 10분마다 Watch 스캔 (개발 환경)
    'scan-watches-every-10-minutes': {
        'task': 'alerts.scan_watches',
        'schedule': crontab(minute='*/10'),  # 0, 10, 20, 30, 40, 50분
    },
    # 매일 자정에 정리 작업
    'cleanup-daily': {
        'task': 'alerts.cleanup_old_data',
        'schedule': crontab(hour=0, minute=0),  # 매일 자정
    },
}

# 태스크 설정
app.conf.task_routes = {
    'alerts.*': {'queue': 'alerts'},
    'catalog.*': {'queue': 'catalog'},
}

# 태스크 결과 설정
app.conf.task_ignore_result = False
app.conf.task_store_errors_even_if_ignored = True

# 워커 설정
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_max_tasks_per_child = 1000

# 디버그 태스크
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """디버그용 태스크"""
    print(f'Request: {self.request!r}')


@app.task(bind=True)
def test_celery_connection(self):
    """Celery 연결 테스트 태스크"""
    return {
        'status': 'success',
        'message': 'Celery 연결 성공',
        'task_id': self.request.id,
        'timestamp': self.request.timestamp
    }
