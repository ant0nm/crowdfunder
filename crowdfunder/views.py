from crowdfunder.models import Profile, Project, Reward, Donation, Category, Tag, Tagging
from crowdfunder.forms import ProjectForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from crowdfunder.forms import LoginForm, ProfileForm, RewardForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse

def root(request):
    return HttpResponseRedirect('/projects/')

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()
    context = {'form': form}
    response = render(request, 'login.html', context)
    return HttpResponse(response)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

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
            return HttpResponseRedirect(reverse('user_profile'))
    else:
        form = UserCreationForm()
    html_response = render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)

def project_page(request):
    context = {'projects': Project.objects.all()}
    return render(request, 'projects.html', context)

def show_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    rewards = project.rewards.all()
    context = {'project': project, 'rewards': rewards}
    html_response = render(request, 'project_details.html', context)
    return HttpResponse(html_response)

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        project = form.instance
        project.owner = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

def profile(request):
    context = {'title': 'Profile'}
    if not Profile.exists_for_user(request.user):
        form = ProfileForm()
        context['form'] = form
    else:
        profile = request.user.profile
        # import ipdb; ipdb.set_trace()
        context['profile'] = profile
        context['first_name'] = profile.first_name
    return render(request, 'profile.html', context)

    # context = {'profile': profile}
    # response = render(request, 'profile.html', context)
    # return HttpResponse(response)


def profile_viewer(request, id):
    profile = Profile.objects.get(pk=id)
    context = {'title': 'Profile', 'profile': profile}
    if not Profile.exists_for_user(request.user):
        form = ProfileForm()
        context['form'] = form
    return render(request, 'profile.html', context)


def profile_create(request):
    user = request.user
    form = ProfileForm(request.POST)
    form.instance.user = request.user
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/profile/')
    else:
        context = {'title': 'Profile', 'form': form}
        return render(request, 'profile.html', context)

def reward_create(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.method == "POST":
        form = RewardForm(request.POST)
        reward = form.instance
        reward.project = project
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('show_project', args=[project_id]))
    else:
        form = RewardForm()
    context = {'project': project, 'form': form}
    return render(request, 'create_reward.html', context)

@login_required
def donate(request):
    if not bool(request.POST):
        raise Http404("If you are the project's owner, you cannot donate to this project. If you are not the owner, please select a reward and donate.")
    else:
        reward_id = int(request.POST['chosen_reward'])
        reward = Reward.objects.get(pk=reward_id)
        project = reward.project
        if reward.within_limit():
            if project.owner != request.user:
                new_donation = Donation.objects.create(user=request.user, reward=reward)
                return HttpResponseRedirect(reverse('show_project', args=[project.pk]))
            else:
                raise Http404("You are the owner, so you cannot donate to this project!")
        else:
            messages.add_message(request, messages.INFO, 'No more {} left :( Pick a different reward!'.format(reward.name))
            return HttpResponseRedirect(reverse('show_project', args=[project.pk]))

def categories_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    html_response = render(request, 'categories.html', context)
    return HttpResponse(html_response)

def category_show(request, category_id):
    category = Category.objects.get(pk=category_id)
    context = {'category': category}
    html_response = render(request, 'category.html', context)
    return HttpResponse(html_response)

def tags_list(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    html_response = render(request, 'tags.html', context)
    return HttpResponse(html_response)

def tag_show(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    context = {"tag": tag}
    html_response = render(request, 'tag.html', context)
    return HttpResponse(html_response)
