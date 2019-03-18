from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "projects_owned")
    name = models.CharField(max_length=255)
    description = models.TextField()
    funding_start_date = models.DateField()
    funding_end_date = models.DateField()
    goal = models.IntegerField()


class Reward(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="rewards")
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    value = models.IntegerField()


class Donation(models.Model):
    user = models.ForeignKey(User, related_name='doantions', on_delete=models.CASCADE)
    reward = models.ForeignKey(Project, related_name='reward', on_delete=models.CASCADE)
