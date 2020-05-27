import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from multi_email_field.fields import MultiEmailField

# Create your models here.


class Profile(models.Model):
    username = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    about = models.TextField(default='nothing here')
    first_flag = models.IntegerField(default=0)

    def __str__(self):
        return self.email


class thots(models.Model):
    uname = models.CharField(max_length=255, null=True)
    head = models.CharField(max_length=255)
    thought = models.TextField()
    thought_on = models.DateTimeField('Date thought on.', auto_now_add=True)
    active = models.BooleanField(default=True)
    #reads = models.ManyToManyField(User, related_name='reads')

    # @property
    # def total_reads(self):
    #     return self.reads.count()

    class Meta:
        ordering = ['-thought_on']

    def __str__(self):
        return self.head


class Likes(models.Model):
    thought = models.ForeignKey(
        thots, on_delete=models.CASCADE, related_name='likes')
    liked_by = models.EmailField(null=True)
    liked = models.BooleanField(default=False)

    class Meta:
        ordering = ['-liked_by']

    def __str__(self):
        return self.liked_by


class Relates(models.Model):
    related_by_name = models.CharField(max_length=255, null=True)
    thought = models.ForeignKey(
        thots, on_delete=models.CASCADE, related_name='relates')
    relating = models.TextField(max_length=1000)
    related_on = models.DateTimeField('Date related on.', auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-related_on']

    def __str__(self):
        return self.relating
