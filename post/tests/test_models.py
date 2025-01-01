from django.contrib.auth import get_user_model
import factory
import pytest
from rest_framework.reverse import reverse

from .factories import UserFactory , PostFactory

@pytest.mark.django_db
def test_user_factory(user):
    assert isinstance(user, get_user_model())
    assert user.is_staff is True

@pytest.mark.parametrize(
    "all_values",
    [
        ("A book description", "book-slug", True ),
    ]
)
def test_post_factory(db, all_values , user):
    description, slug, status= all_values
    author = user
    post = PostFactory(
        author  = author ,
        description = description ,
        slug = slug,
        status = status,
        image=factory.django.ImageField(from_=factory.Faker('image_url'))
    )
    assert post.author == author
    assert post.description == "A book description"
    assert post.slug == "book-slug"
    assert post.status == True
    assert len(post.likes.all()) >= 0
    assert post.image.size > 0
    assert post.image.name.endswith('.jpg')
    post.delete()


