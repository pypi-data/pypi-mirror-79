from .abstract_user import AbstractUser


class EmailUser(AbstractUser):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
