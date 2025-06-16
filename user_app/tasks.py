# from celery import shared_task

from django.utils import timezone
from datetime import timedelta
from .models import VerificationCode
import time
# @shared_task
def delete_old_code(code_id):
    time.sleep(1000)
    try:
        code = VerificationCode.objects.get(id=code_id)
        code.delete()
    except:
        pass