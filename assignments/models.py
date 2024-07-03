from django.db import models
from django.utils import timezone
from users.models import User, Subject
from batches.models import Batch
# Create your models here.

class Lecture(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video_links = models.TextField(blank=True, null=True)  # Assuming 'text[]' means array of text, Django doesn't support array fields natively. You might need to use JSONField or a third-party library for this.
    additional_resource = models.TextField(blank=True, null=True)  # Assuming 'text[]' means array of text, Django doesn't support array fields natively. You might need to use JSONField or a third-party library for this.
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_lectures')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_lectures')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lectures')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_lectures')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_lectures')


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tags')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_tags')
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LectureTagMapping(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='lecture_tag_mappings')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='lecture_tag_mappings')
    is_deleted = models.BooleanField(default=False)


class RecordedVideo(models.Model):
    id = models.AutoField(primary_key=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='recorded_videos')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='recorded_videos')
    video_links = models.TextField(blank=True, null=True)  # Assuming 'text ARRAY' means array of text, Django doesn't support array fields natively. You might need to use JSONField or a third-party library for this.
    is_deleted = models.BooleanField(default=False)


class StudentRecordedRequest(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('allowed', 'Allowed'), ('rejected', 'Rejected'), ('expired', 'Expired')]
    
    id = models.AutoField(primary_key=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='student_recorded_requests')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='student_recorded_requests')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    reason = models.CharField(max_length=200)
    topic = models.CharField(max_length=100, blank=True, null=True)
    goal = models.CharField(max_length=250, blank=True, null=True)
    total_lectures = models.IntegerField(default=0)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='changed_student_recorded_requests')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')
    is_deleted = models.BooleanField(default=False)


class Assignment(models.Model):
    STATUS_CHOICES = [('publish', 'Publish'), ('draft', 'Draft')]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='draft')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

class AssignmentQuestions(models.Model):
    TYPE_CHOICES = [('mcq', 'MCQ'), ('subjective', 'Subjective'), ('multiple_correct', 'Multiple Correct')]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    penalty = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='mcq')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='inactive')
    is_deleted = models.BooleanField(default=False)

class AssignmentTagMapping(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

class AssignmentQuestionTagMapping(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    assignment_question = models.ForeignKey(AssignmentQuestions, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

class AssignmentQuestionOptions(models.Model):
    id = models.AutoField(primary_key=True)
    option = models.TextField()
    question = models.ForeignKey(AssignmentQuestions, on_delete=models.CASCADE)
    is_correct = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

class AssignmentAttempts(models.Model):
    STATUS_CHOICES = [('correct', 'Correct'), ('incorrect', 'Incorrect'), ('not_attempted', 'Not Attempted')]
    id = models.AutoField(primary_key=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(AssignmentQuestions, on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=13, choices=STATUS_CHOICES, default='not_attempted')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)


class AssignmentMetaInfo(models.Model):
    id = models.AutoField(primary_key=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    total_questions = models.IntegerField()
    total_student_attempted = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

class AssignmentQuestionsMetaInfo(models.Model):
    id = models.AutoField(primary_key=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    assignment_question = models.ForeignKey(AssignmentQuestions, on_delete=models.CASCADE)
    total_correct = models.IntegerField(default=0)
    total_incorrect = models.IntegerField(default=0)
    total_not_attempted = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

class AssignmentBatchMapping(models.Model):
    id = models.AutoField(primary_key=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)


class Library(models.Model):
    STATUS_CHOICES = [('publish', 'Publish'), ('draft', 'Draft'), ('trash', 'Trash')]
    TYPE_CHOICES = [('public', 'Public'), ('private', 'Private')]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='libraries_created', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='libraries_updated', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='inactive')
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='private')
    is_global = models.SmallIntegerField(default=0)
    batch = models.ForeignKey(Batch, null=True, blank=True, on_delete=models.SET_NULL)