from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone

class Category(models.Model):
    category_name = models.CharField(verbose_name='categories', max_length=100)

    def __str__(self):
        return self.category_name

class Folder(models.Model):
    folder_name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.folder_name

class File(models.Model):
    # folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100)
    uploaded_by  = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    file_size = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file_name

class TableFile(models.Model):
    accusor_name = models.CharField(max_length=255, verbose_name='ከሳሽ መልስ ሰጭ')
    defendent_name = models.CharField(max_length=255, verbose_name='ተከሳሽ መልስ  ሰጭ')
    house_number = models.CharField(max_length=255, verbose_name='የቤት ቁጥር')
    id_number = models.CharField(max_length=255, verbose_name='የመ.ቁ ')
    court_house = models.CharField(max_length=255, verbose_name='ክርክሩ የነበረበት ፍ/ቤት')
    debate_type = models.CharField(max_length=255, verbose_name='የክርክሩ አይነት')
    date_archive_initiated = models.DateTimeField(auto_now_add=False, verbose_name='መዝገቡ የመጣበት ቀን')
    date_court_decision_made = models.DateTimeField(auto_now_add=False, verbose_name='ፍርድ ቤቱ ውሳኔ የሰጠበት ቀን')
    date_court_decision_copy_sent = models.DateTimeField(auto_now_add=False, verbose_name='የውሳኔ ግልባጭ የተላከበት ቀን')
    status = models.CharField(max_length=255, verbose_name='በፍ/ቤቱ ውሳኔ መሰረት ተፈፅሞል/አልተፈፀመም')
    prosecutor = models.CharField(max_length=255, verbose_name='ጉዳዩን የያዘው ዐቃቤ ህግ ስም')

    def __str__(self):
        return self.prosecutor
    


# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, role='user', **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, role=role, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None, role='admin', **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(username, email, password, role, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=30, unique=True)
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     phone_number = models.CharField(max_length=30)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)
#     role = models.CharField(max_length=20, default='user') 

#     groups = models.ManyToManyField(
#         Group,
#         verbose_name='groups',
#         blank=True,
#         related_name='custom_users'  # Add this related_name
#     )

#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user permissions',
#         blank=True,
#         related_name='custom_users'  # Add this related_name
#     )

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

#     def __str__(self):
#         return self.username


