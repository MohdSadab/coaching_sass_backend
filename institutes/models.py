from django.db import models
from users.models import User

# Create your models here.

class Institute(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=250)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=1000, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    logo = models.TextField(blank=True, null=True)  # Assuming 'text[]' means array of text, Django doesn't support array fields natively. You might need to use JSONField or a third-party library for this.
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='created_users')
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='updated_users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    

class Achievement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=1000, blank=True, null=True)
    images = models.TextField(blank=True, null=True)  # Assuming 'text[]' means array of text, Django doesn't support array fields natively. You might need to use JSONField or a third-party library for this.
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='achievements')
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class InstitutesUserMapping(models.Model):
    id = models.AutoField(primary_key=True)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='institutes_user_mappings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='institutes_user_mappings')
    is_admin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)