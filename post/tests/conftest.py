import pytest
from django.contrib.auth import get_user_model
from post.tests.factories import UserFactory , PostFactory
from django.conf import settings
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return UserFactory()
@pytest.fixture
def post():
    return PostFactory



@pytest.fixture
def superuser(db):
    User = get_user_model()

    # Create a superuser
    superuser = User.objects.create_superuser(
        username=settings.TEST_SUPERUSER_USERNAME,
        email=settings.TEST_SUPERUSER_EMAIL,
        password=settings.TEST_SUPERUSER_PASSWORD
    )

    # Ensure the superuser is staff and active
    superuser.is_staff = True
    superuser.is_active = True
    superuser.save()

    return superuser