from django.contrib.auth.models import User
from django.db import models

class UserRecord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)

    def __str__(self):
        return self.first_name

class UserImages(models.Model):
    user_record = models.ForeignKey(UserRecord, on_delete=models.CASCADE)
    fancy_dress = models.ImageField(upload_to='user_uploads/fancy_dress', null=True, blank=True)
    drawing = models.ImageField(upload_to='user_uploads/drawing', null=True, blank=True)
    essay_writing = models.ImageField(upload_to='user_uploads/essay_writing', null=True, blank=True)

    def __str__(self):
        return f"Images for {self.user_record.email}'s record"
