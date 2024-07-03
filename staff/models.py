from django.db import models
from institutes.models import Institute
from users.models import User

# Create your models here.
class Teachers(models.Model):
    id = models.AutoField(primary_key=True)
    institute_id = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='institutes')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_institutes')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_institutes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


