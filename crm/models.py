from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=150)
    about = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)

    @property
    def amount_offices(self):
        return self.offices.count()

    def __str__(self):
        return f'{self.name}'


class Office(models.Model):
    name = models.CharField(max_length=150)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='offices', blank=True, null=True)
    location = CountryField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} company - {self.company.name}'

    @property
    def amount_workers(self):
        return self.workers.count()


class Worker(models.Model):
    employer = models.ForeignKey('Profile', on_delete=models.CASCADE)
    company = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='workers')
    position = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.employer.name} company - {self.company.name}, position is {self.position}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True)
    surname = models.CharField(max_length=150, null=True)
    patronymic = models.CharField(max_length=150, null=True)
    bio = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} name - {self.name}, surname - {self.surname} '


class UserSkill(models.Model):
    skill = models.CharField(max_length=150)
    level = models.SmallIntegerField(default=0)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return f'{self.user.name} {self.skill} level {self.level}'


class UserLanguage(models.Model):
    language = models.CharField(max_length=150)
    level = models.SmallIntegerField(default=0)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='languages')

    def __str__(self):
        return f'{self.user.name} {self.language} level {self.level}'
