from django.contrib.auth import get_user_model

from ..models import OtpModel
from ..tasks import send_review_email_task
from django.utils import timezone
from datetime import datetime, timedelta
import random
from ..utils.Epoch import Epoch
from ..services.user import UserService
from rest_framework import status
from rest_framework.response import Response


class OtpService:
    @classmethod
    def get_delta_time(cls) -> datetime:
        expire_time = 120  # second

        delta_time = timezone.now() - timedelta(seconds=expire_time)

        return delta_time

    @classmethod
    def generate(cls) -> str:
        token = list(str(Epoch.microsecond_now())[-6:])
        random.shuffle(token)
        return ''.join(token)

    @classmethod
    def request(cls , email):
        delta_time = cls.get_delta_time()

        otp_objs = OtpModel.objects.filter(
            email=email,
            created__gte=delta_time,
        ).order_by('-created')

        if otp_objs.exists():
            otp_obj = otp_objs.first()
        else:
            code = cls.generate()
            otp_obj = OtpModel.objects.create(
                code=code,
                email=email,
            )
            send_review_email_task.delay(email=email,code=code)
        return int(abs(delta_time - otp_obj.created).total_seconds())
    @classmethod
    def verify(cls,  code: str, email: str = None):
        delta_time = cls.get_delta_time()

        OtpModel.objects.filter(
            email=email,
            created__lt=delta_time,
        ).delete()

        otp_objs = OtpModel.objects.filter(
            code=code,
            email=email,
            created__gte=delta_time,
        )

        if otp_objs.exists():
            user_obj = UserService.detail(email)

            return user_obj

        return None