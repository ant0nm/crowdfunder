from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @classmethod
    def exists_for_user(self, user):
        return Profile.objects.filter(user_id=user.id).exists()

    def has_backed(self):
        user_projects = []
        for donation in self.user.donations.all():
            reward = donation.reward
            if reward.project not in user_projects:
                user_projects.append(reward.project)
        return user_projects

    def total_donations(self):
        total = 0
        donations = self.user.donations.all()
        for donation in donations:
            total += donation.reward.value
        return total


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "projects_owned")
    name = models.CharField(max_length=255)
    description = models.TextField()
    funding_start_date = models.DateField()
    funding_end_date = models.DateField()
    goal = models.IntegerField()

    def total_funds(self):
        total = 0
        for reward in self.rewards.all():
            total += reward.number_donated() * reward.value
        return total

class Reward(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="rewards")
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    value = models.IntegerField()

    def number_donated(self):
        return self.donations.count()


class Donation(models.Model):
    user = models.ForeignKey(User, related_name='donations', on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, related_name='donations', on_delete=models.CASCADE)
