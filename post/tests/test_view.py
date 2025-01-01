import factory
import pytest
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse
from .factories import PostFactory


@pytest.mark.parametrize(
    "all_values",
    [
        ("A book description", "book-slug", True ),
    ]
)
def test_read_posts( db,client , user , all_values):
    description, slug, status= all_values
    author = user
    post = PostFactory(
        author  = author ,
        description = description ,
        slug = slug,
        status = status,
        image=factory.django.ImageField(from_=factory.Faker('image_url'))
    )
    url = reverse('apipost:list')
    response = client.get(url)
    print("len" , len(response.data))
    type(len(response.data))
    assert response.status_code == 200
    assert len(response.data) == 1


def test_retrieve_404(db , client , user ):
    url = reverse('apipost:detail', kwargs={'pk':10})
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.parametrize(
    "all_values",
    [
        ("A book description", "book-slug", True ),
    ]
)
def test_detail(db , client , user , all_values):
    description, slug, status= all_values
    author = user
    post = PostFactory(
        author  = author ,
        description = description ,
        slug = slug,
        status = status,
        image=factory.django.ImageField(from_=factory.Faker('image_url'))
    )
    url = reverse('apipost:detail', kwargs={'pk':post.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "all_values",
    [
        ("A book description", "book-slug", True ),
    ]
)
def test_update(db , client , superuser , all_values):
    description, slug, status= all_values
    author = superuser
    post = PostFactory(
        author  = author ,
        description = description ,
        slug = slug,
        status = status,
        image=factory.django.ImageField(from_=factory.Faker('image_url'))
    )
    url = reverse('apipost:update', kwargs={'pk':post.pk})
    payload = dict(slug = "new-slug" , status = False)
    client.force_authenticate(user=superuser)
    response = client.patch(url , payload)
    data = response.data
    assert response.status_code == 200
    assert data.get('slug') == "new-slug"
    assert data.get('status') == False

@pytest.mark.parametrize(
    "all_values",
    [
        ("A book description", "book-slug", True ),
    ]
)
def test_delete(db , client , superuser , all_values):
    description, slug, status= all_values
    author = superuser
    post = PostFactory(
        author  = author ,
        description = description ,
        slug = slug,
        status = status,
        image=factory.django.ImageField(from_=factory.Faker('image_url'))
    )
    url = reverse('apipost:delete', kwargs={'pk':post.pk})
    client.force_authenticate(user=superuser)
    response = client.delete(url)
    assert response.status_code == 204