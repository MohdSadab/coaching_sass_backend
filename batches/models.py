from django.db import models
from institutes.models import Institute
from users.models import User

class Batch(models.Model):
    REGISTRATION_STATUS_CHOICES = [('open', 'Open'), ('closed', 'Closed')]
    MEDIUM_CHOICES = [('hinglish', 'Hinglish'), ('english', 'English')]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, blank=True, null=True)
    total_students = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_status = models.CharField(max_length=6, choices=REGISTRATION_STATUS_CHOICES, default='open')
    timing = models.CharField(max_length=200, blank=True, null=True)
    batch_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    medium = models.CharField(max_length=8, choices=MEDIUM_CHOICES, default='english')
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='batches')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_batches')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_batches')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserBatchMapping(models.Model):
    id = models.AutoField(primary_key=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='user_batch_mappings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_batch_mappings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_user_batch_mappings')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_user_batch_mappings')


class BatchLecturePlan(models.Model):
    STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published')]

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_lecture_plans')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    description = models.CharField(max_length=1000, blank=True, null=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='changed_batch_lecture_plans')
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='draft')
    is_deleted = models.BooleanField(default=False)