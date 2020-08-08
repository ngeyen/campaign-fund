from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, username, password):
        if not email:
            raise ValueError("please enter an email")
        if not first_name:
            raise ValueError('First name is required')
        if not last_name:
            raise ValueError('Last name is required')
        if not username:
            raise ValueError('username is required')
        if not password:
            raise ValueError('Password is required')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        if not email:
            raise ValueError("please enter an email")
        if not first_name:
            raise ValueError('First name is required')
        if not last_name:
            raise ValueError('Last name is required')
        if not username:
            raise ValueError('username is required')
        if not password:
            raise ValueError('Password is required')
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name      = models.CharField(verbose_name='first name', max_length=50)
    last_name       = models.CharField(verbose_name='last name', max_length=50)
    disp_pic        = models.ImageField(verbose_name='display-pic', upload_to='images/profile/', blank=False, null=False,
                                 default='images/profile/user.png')
    email           = models.EmailField(verbose_name='email', max_length=100, unique=True)
    username        = models.CharField(max_length=30, blank=False, null=False, default=first_name, unique=True)
    password        = models.CharField(max_length=255, verbose_name='password')

    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', ]

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Visitor(models.Model):
    name = models.CharField(verbose_name='Full name ', max_length=150)
    email = models.EmailField(verbose_name='email', max_length=254)

    def __str__(self):
        return self.name


class Coordinator(AbstractBaseUser):
    first_name      = models.CharField(verbose_name='first name', max_length=50)
    last_name       = models.CharField(verbose_name='last name', max_length=50)
    email           = models.EmailField(verbose_name='email', max_length=100, unique=True)
    username        = models.CharField(max_length=30, blank=False, null=False, default=first_name, unique=True)
    password        = models.CharField(max_length=255, verbose_name='password')

    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=True)
    is_superuser    = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', ]

    def has_perm(self, perm, obj=None):
        return self.is_staff
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    

class CoordinatorManager(BaseUserManager):
    def create_coordinator(self, first_name, last_name, email, username, password):
        if not email:
            raise ValueError("please enter an email")
        if not first_name:
            raise ValueError('First name is required')
        if not last_name:
            raise ValueError('Last name is required')
        if not username:
            raise ValueError('username is required')
        if not password:
            raise ValueError('Password is required')

        coordinator = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,

        )
        coordinator.is_admin = True
        coordinator.is_staff = True
        coordinator.is_superuser = False
        coordinator.set_password(password)
        coordinator.save(using=self._db)
        return coordinator