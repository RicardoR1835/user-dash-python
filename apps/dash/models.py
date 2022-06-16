from __future__ import unicode_literals
from django.db import models
import re
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        context = {
            "users": User.objects.all()
        }
        grab = User.objects.filter(email=postData['email'])
        if len(postData['fn']) < 2:
            errors["fn"] = "First name should be more than 2 characters"
        if len(postData['ln']) < 2:
            errors['ln'] = "Last name should be more than 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email not entered in correct form"
        if len(grab) > 0:
            errors['email1'] = "Email already exists"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if postData['password'] != postData['password_confirm']:
            errors["password_confirm"] = "Passwords do not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        context = {
            "users": User.objects.all()
        }
        email = User.objects.filter(email=postData['email'])
        if len(email) == 0:
            errors["log-email"] = "Email is not registered"
        else:
            user = User.objects.get(email=postData['email'])
            if user.password != postData['password']:
                errors["log-pass"] = "Invalid Credentials"
        return errors

    def edit_validator(self, postData):
        errors = {}
        context = {
            "users": User.objects.all()
        }
        user = User.objects.filter(id=postData['id'])
        if len(postData['fn']) < 2:
            errors["fn"] = "First name should be more than 2 characters"
        if len(postData['ln']) < 2:
            errors['ln'] = "Last name should be more than 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email not entered in correct form"
        return errors

    def pw_validator(self, postData):
        errors = {}
        context = {
            "users": User.objects.all()
        }
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if postData['password'] != postData['password_confirm']:
            errors["password_confirm"] = "Passwords do not match"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
    def __repr__(self):
        return f"<Users object: {self.id} ({self.email})>"

class Message(models.Model):
    message = models.TextField()
    created_by = models.ForeignKey(User, related_name="created_messages", on_delete=models.CASCADE, blank=True, null=True)
    created_for = models.ForeignKey(User, related_name="my_messages", on_delete=models.CASCADE, blank=True, null=True)
    likes_on_messages = models.ManyToManyField(User, related_name="messages_liked")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Comment(models.Model):
    comment = models.TextField()
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    likes_on_comment = models.ManyToManyField(User, related_name="comments_liked")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)