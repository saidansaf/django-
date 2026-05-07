from django.db import models

from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.text import slugify
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email bo'lishi shart")
        # email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        return self.create_user(email,password,**extra_fields)


class CustomUser(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name', 'last_name']
    phone_number=models.CharField(max_length=50, blank=False, null=False)
    slug=models.SlugField(unique=True, blank=True)
    picture=models.ImageField(upload_to='media/', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    objects=CustomUserManager()

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(f"{self.first_name}-{self.last_name}-{str(uuid.uuid4())[:8]}")

        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
