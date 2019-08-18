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
    profile_skill = models.CharField(max_length=50,)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_absolute_url(self):
        return reverse('profile:my_profile')


class Project(models.Model): #article
    project_skill = models.CharField(max_length=400)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(max_length=300)
    title = models.CharField(max_length=100)
    timeline = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class ProjectPosition(models.Model):
    #one project can have many positions
    project = models.ForeignKey(Project, on_delete=models.CASCADE,)
    title = models.CharField(max_length=300, blank=True)
    information = models.TextField(max_length=300, blank=True)
    apply = models.BooleanField(default=False)
    timeline = models.CharField(max_length=20)
    filled = models.BooleanField(default=False)
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.title


class Applicant(models.Model):

    ACCEPTED = 'a'
    REJECTED = 'r'
    PENDING = 'p'
    STATUS_CHOICES = (
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (PENDING, 'Pending'),
    )

    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,)
    position = models.ForeignKey('ProjectPosition', on_delete=models.CASCADE)


class ProfileSkill(models.Model):
    skill_name = models.CharField(max_length=50, blank=True)
    # one profile can have many skills
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,)

    def __str__(self):
        return self.skill_name


class ProjectSkill(models.Model):
    name = models.CharField(max_length=50)
    # one profile can have many skills
    project = models.ForeignKey(Project, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name
