from django.contrib.auth.models import User
from django.db import models
from datetime import date

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

    def fully_funded(self):
        if self.total_funds() >= self.goal:
            return True
        else:
            return False

    def expired(self):
        return date.today() > self.funding_end_date

    def status(self):
        if self.expired():
            if self.fully_funded():
                return "The project has already expired, but it has met its funding goal."
            else:
                return "The project has already expired, however it has not met its funding goal."
        else:
            if self.fully_funded():
                return "The project is still open, and it's already met its funding goal!"
            else:
                return "The project is still open, however it has not met its funding goal yet."

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
