from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('premium', 'Premium'),
    ]

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    ]

    STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('deleted', 'Deleted'),
        ('blocked', 'Blocked'),
        ('pending_verification', 'Pending Verification'),
    ]

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=1000)
    salt = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='free')
    verified = models.BooleanField(default=False)
    profile_img = models.CharField(max_length=1000, blank=True, null=True)
    street = models.CharField(max_length=1000, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    standard = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    last_logged_in = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_verification')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

class UserSubjectMapping(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='user_subject_mappings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_subject_mappings')
    is_deleted = models.BooleanField(default=False)


class EducationDetail(models.Model):
    id = models.AutoField(primary_key=True)
    std_name = models.CharField(max_length=255)
    stream = models.CharField(max_length=255)
    passing_date = models.DateField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Assuming percentage can have 2 decimal places
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education_details')
    is_deleted = models.BooleanField(default=False)