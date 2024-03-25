from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    contact_info = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.name}"
    
class Product(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    imgurl = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    date = models.DateTimeField(default=datetime.now)
    curprice = models.IntegerField(default=0)
    byuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="byuser", default=None, null=True)
    
    def __str__(self):
        return f"{self.title}"
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(max_length=100)


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField()
    bio = models.TextField()
    # Add more fields as needed, such as photo, etc.

    def __str__(self):
        return self.name
