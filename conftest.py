import pytest
from post.tests.factories import UserFactory , PostFactory
from pytest_factoryboy import register

register(UserFactory)
register(PostFactory)