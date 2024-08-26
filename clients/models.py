from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from PIL import Image
import os

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'countries'

class State(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, related_name='states', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} state' 
    
class City(models.Model):
    name = models.CharField(max_length=200)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} city'
    
    class Meta:
        verbose_name_plural = 'cities'
    
SELECT = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('others', 'others'),
    ('PNT', 'prefer_not_to_mention'),
]

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/avatars', default='images/logo4.PNG', null=True, blank=True)
    country = models.ForeignKey(Country, verbose_name='country', on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, verbose_name='state', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, verbose_name='city', on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(choices=SELECT, default='PNT', blank=True, max_length=100)
    occupation = models.CharField(max_length=300, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar and os.path.exists(self.avatar.path):

            sit = Image.open(self.avatar.path)

            if sit.height > 250 or sit.width > 250:
                output_size = (250, 250)
                sit.thumbnail(output_size)
                sit.save(self.avatar.path)

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Client(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)


class Testimonial(models.Model):
    testimony = RichTextField(null=True, blank=True)
    testifier = models.CharField(max_length=200, unique=False)
    photo = models.ImageField(upload_to='uploads/testimony', default='images/logo5.PNG', blank=True)
    occupation = models.CharField(max_length=200)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'testimony by: {self.testifier}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.photo and os.path.exists(self.photo.path):

            git = Image.open(self.photo.path)

            if git.height > 250 or git.width > 250:
                output_size = (250, 250)
                git.thumbnail(output_size)
                git.save(self.photo.path)

