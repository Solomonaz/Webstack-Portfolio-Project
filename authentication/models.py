from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name,phone_number,role, username, email, profile_picture, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have user name')
        
        user = self.model(
            email  =self.normalize_email(email),
            username =username,
            first_name =first_name,
            last_name   =last_name,
            phone_number = phone_number,
            role = role,
            profile_picture = profile_picture,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name,phone_number, role, username, email, password):
        user =self.create_user(
            email  =self.normalize_email(email),
            password =password,
            username =username,
            first_name =first_name,
            last_name   =last_name,
            phone_number = phone_number,
            role = role,
        )
        user.is_admin =True
        user.is_active =True
        user.is_staff =True
        user.is_superadmin =True
        user.save(using=self._db)
        return user
 

class Account(AbstractBaseUser):
    ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLES, default='admin')
    
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now_add=True)
    
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile/', default='profile/default.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    objects = MyAccountManager()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
