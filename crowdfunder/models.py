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

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "projects_owned")
    name = models.CharField(max_length=255)
    description = models.TextField()
    funding_start_date = models.DateField()
    funding_end_date = models.DateField()
    goal = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="projects")
    tags = models.ManyToManyField(Tag, through='Tagging', related_name='projects')

    def __str__(self):
        return self.name

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

    def funding_deadline(self):
        time_remaining = (self.funding_end_date - date.today())
        return time_remaining.days

class Tagging(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="taggings")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="taggings")

class Reward(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="rewards")
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    value = models.IntegerField()
    max_donations = models.IntegerField()

    def __str__(self):
        return self.name

    def number_donated(self):
        return self.donations.count()

    def within_limit(self):
        num_of_donations = self.number_donated()
        return num_of_donations < self.max_donations

    def rewards_left(self):
        return self.max_donations - self.number_donated()

class Donation(models.Model):
    user = models.ForeignKey(User, related_name='donations', on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, related_name='donations', on_delete=models.CASCADE)
