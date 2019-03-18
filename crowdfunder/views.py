from crowdfunder.models import Profile, Project, Reward, Donation
from crowdfunder.forms import ProjectForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from crowdfunder.forms import LoginForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

def root(request):
    return HttpResponseRedirect('/projects/')

def login_view(request):
    pass

def logout_view(request):
    pass

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('profile/')
    else:
        form = UserCreationForm()
    html_response = render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)

def project_page(request):
    context = {'projects': Project.objects.all()}
    return render(request, 'projects.html', context)

def show_project(request, project_id):
    pass

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        project = form.instance
        project.owner = request.user
        if form.is_valid():
            form.save()
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

def profile(request):
    context = {'title': 'Profile'}
    if not Profile.exists_for_user(request.user):
        form = ProfileForm()
        context['form'] = form
    return render(request, 'profile.html', context)

def profile_create(request):
    form = ProfileForm(request.POST)
    form.instance.user = request.user
    if form.is_valid():
        form.save()
        return redirect(reverse('user_profile'))
    else:
        context = {'title': 'Profile', 'form': form}
        return render(request, 'profile.html', context)
