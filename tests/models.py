from django.db import models
from django.utils import timezone
from users.models import User

class Test(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    TYPE_CHOICES = [('public', 'Public'), ('private', 'Private')]
    TEST_FEE_STATUS_CHOICES = [('paid', 'Paid'), ('not_paid', 'Not Paid')]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    duration = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tests')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_tests')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='inactive')
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='private')
    is_global = models.SmallIntegerField(default=0)
    test_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    test_fee_status = models.CharField(max_length=8, choices=TEST_FEE_STATUS_CHOICES, default='not_paid')
    test_fee_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_deleted = models.BooleanField(default=False)


class Sections(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_sections')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_sections')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='inactive')
    total_marks = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

# Define other models in a similar way...

class TestQuestions(models.Model):
    TYPE_CHOICES = [('mcq', 'MCQ'), ('subjective', 'Subjective'), ('multiple_correct', 'Multiple Correct')]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    question = models.TextField()
    section = models.ForeignKey(Sections, on_delete=models.CASCADE)
    marks = models.IntegerField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    penalty = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    type = models.CharField(max_length=18, choices=TYPE_CHOICES, default='mcq')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='inactive')
    is_deleted = models.BooleanField(default=False)


class TestOptions(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    option = models.TextField()
    question = models.ForeignKey(TestQuestions, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='inactive')
    is_correct = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

class TestAttempts(models.Model):
    STATUS_CHOICES = [('correct', 'Correct'), ('incorrect', 'Incorrect'), ('not_attempted', 'Not Attempted')]
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Sections, on_delete=models.CASCADE)
    question = models.ForeignKey(TestQuestions, on_delete=models.CASCADE)
    option = models.ForeignKey(TestOptions, on_delete=models.CASCADE, null=True, blank=True)
    marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=13, choices=STATUS_CHOICES, default='not_attempted')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

# Continue defining other models...

class TestResults(models.Model):
    STATUS_CHOICES = [('pass', 'Pass'), ('fail', 'Fail')]
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    obtained_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    rank = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='fail')
    attempted = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

class TestMetaInfo(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    total_questions = models.IntegerField()
    total_sections = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

class TestQuestionsMetaInfo(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    test_question = models.ForeignKey(TestQuestions, on_delete=models.CASCADE)
    total_correct = models.IntegerField(default=0)
    total_incorrect = models.IntegerField(default=0)
    total_not_attempted = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)