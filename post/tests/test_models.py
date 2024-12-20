from django.contrib.auth import get_user_model
import factory
import pytest
from .factories import UserFactory , PostFactory

@pytest.fixture
def user_factory():
    return UserFactory()

@pytest.mark.django_db
def test_user_factory(user_factory):
    print(user_factory.username)
    assert isinstance(user_factory, get_user_model())
    assert user_factory.is_staff is True

@pytest.mark.parametrize(
    "all_values",
    [
        ("A book description", "book-slug", True ),
    ]
)
def test_post_factory(db, all_values , user_factory):
    description, slug, status= all_values
    author = user_factory
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
    print("len", len(post.likes.all()))
    assert len(post.likes.all()) >= 0
    assert post.image.size > 0
    assert post.image.name.endswith('.jpg')
    post.delete()



