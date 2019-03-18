from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, DateField, PasswordInput, Form, EmailField
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
