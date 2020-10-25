from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from settings.models import Setting


class MyAccountManager(BaseUserManager):
    def create_user(self, username, name, password=None):
        if not username:
            raise ValueError('Users must have a username')
        if not name:
            raise ValueError('Users must have a name')

        user = self.model(
            username= username,
            name=name,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, is_active=True, password=None):
        user = self.create_user(
            username= username,
            password=password,
            name=name,
        )
        user.is_active = True
        user.is_admin = True
        user.is_ec = True
        user.is_verifier = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(verbose_name="username", max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_ec = models.BooleanField(default=False)
    is_verifier = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    @property
    def get_role(self):
        if self.is_admin and self.is_ec and self.is_verifier:
            return 'Admin'
        elif self.is_ec:
            return 'Commissioner'
        elif self.is_verifier:
            return 'Verifier'

    @property
    def get_setting(self):
        setting = Setting.objects.filter().first()
        return setting

