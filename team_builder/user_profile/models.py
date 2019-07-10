from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse

from team_builder import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_absolute_url(self):
        return reverse('profile:my_profile')


class Skill(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, unique=False)


class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, unique=False)
    description = models.TextField(max_length=300)
    name = models.CharField(max_length=100)
    skills = models.CharField(max_length=100)
    # positions = models.ManyToManyField('Postition', blank=True)

