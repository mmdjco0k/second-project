from django.contrib.auth import get_user_model

User = get_user_model()


class UserService:
    @classmethod
    def detail(cls, email):
        user_objs = User.objects.filter(
            email=email,
        )
        if user_objs.exists():
            return user_objs.first()
        return None