from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('no username provided')
        if not email:
            raise ValueError('no email provided')
        normal_email = self.normalize_email(email)
        user = self.model(username=username, email=normal_email)
        user.set_password(raw_password=password)

        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    bank_account = models.IntegerField(default=100)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=100, primary_key=True)


class Inventory(models.Model):
    seller = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    title = models.ForeignKey(Book, to_field='title', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()


class Cart(models.Model):
    buyer = models.ForeignKey(User,related_name='carts', to_field='username', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    title = models.ForeignKey(Book, to_field='title', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
