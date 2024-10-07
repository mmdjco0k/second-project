from celery import shared_task
from celery.utils.log import get_task_logger
from .services.email import Email

logger = get_task_logger(__name__)

@shared_task
def send_review_email_task(email , code):
    logger.info("sent register email")
    e = Email.send_review_email(email , code)
    if e :
        logger.info("email sent")
        return e

    logger.info("The email was not sent")