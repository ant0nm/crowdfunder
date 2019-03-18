import datetime as dt
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.forms import ModelForm, Form, CharField, DateField, PasswordInput, EmailField, DateInput, IntegerField
from crowdfunder.models import Profile, Project, Reward, Donation
from django import forms

min_zero = MinValueValidator(limit_value=1)

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
    goal = IntegerField(validators=[min_zero])

    class Meta:
        model = Project
        fields = ['name', 'description', 'funding_start_date', 'funding_end_date', 'goal']

    def clean_start_date(self):
        cleaned_date = self.cleaned_data['funding_start_date']
        if cleaned_date < dt.date.today():
            self.add_error('Start date must be in the future.')

    def clean_end_date(self):
        cleaned_start_date = self.cleaned_data['funding_start_date']
        cleaned_end_date = self.cleaned_data['funding_end_date']
        if cleaned_start_date > cleaned_end_date:
            self.add_error('End date must be after start date.')
