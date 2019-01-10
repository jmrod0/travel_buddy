from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors ={}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name cannot be empty'
       
        elif not postData['first_name'].isalpha():
            errors['first_name']= 'First name cannot contain any numbers'
        
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'
        
        elif not postData['last_name'].isalpha():
            errors['last_name'] = 'Last name cannot contain any numbers'
        
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Must be a valid email'
        
        if User.objects.filter(email = postData['email']):
            errors['email']= 'User already exists'
        
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters in length'
        
        if postData['c_password'] != postData['password']:
            errors['c_password'] = 'Passwords must match!'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 100)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Trip(models.Model):
    city = models.CharField(max_length = 100)
    country = models.CharField(max_length = 100)
    start_date = models.DateField()
    end_date = models.DateField()
    travelers = models.ManyToManyField(User, related_name = "trips")
    # planner = models.ForeignKey(User, related_name ='planned_trips', on_delete = models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

# Create your models here.
