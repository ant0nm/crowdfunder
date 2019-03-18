from crowdfunder.models import Profile, Project, Reward, Donation
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

def root(request):
    return HttpResponseRedirect('/projects/')

def login_view(request):
    pass

def logout_view(request):
    pass

def signup(request):
    pass

def project_page(request):
    pass

def show_project(request, project_id):
    pass

def create_project(request):
    pass

def profile(request):
    pass

def profile_create(request):
    pass
