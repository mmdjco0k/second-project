import factory
from django.contrib.auth import get_user_model
from post.models import PostModel
from faker import Faker

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
    username = factory.Faker('name')
    is_staff = True
    is_superuser = True

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostModel
    author = factory.SubFactory(UserFactory)
    description = factory.Faker('text', max_nb_chars=255)
    slug = factory.Faker('text', max_nb_chars=250)
    status = True
    postId = fake.random_int(min=0 , max=10)
    image = factory.django.ImageField(from_=factory.Faker('image_url'))
    class Params:
        @factory.post_generation
        def likes(self, create, extracted, **kwargs):
            if not create:
                return
            num_likes = fake.random_int(min=0, max=10)
            self.likes.set([UserFactory() for _ in range(num_likes)])


