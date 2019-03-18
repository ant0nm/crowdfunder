import datetime as dt
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField, DateField, PasswordInput, EmailField, DateInput
from crowdfunder.models import Profile, Project, Reward, Donation
from django import forms

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

class ProfileForm(ModelForm):
    first_name = CharField()
    last_name = CharField()
    email = EmailField()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email']

class ProjectForm(ModelForm):
    funding_start_date = DateField(widget=DateInput(attrs={'type': 'date', 'min': dt.date.today() }))
    funding_end_date = DateField(widget=DateInput(attrs={'type': 'date', 'min': dt.date.today() }))
    class Meta:
        model = Project
        fields = ['name', 'description', 'funding_start_date', 'funding_end_date', 'goal']

class RewardForm(ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'description', 'value']
