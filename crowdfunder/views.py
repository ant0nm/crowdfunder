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
            return HttpResponseRedirect('/projects/')
    else:
        form = UserCreationForm()
    html_response = render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)

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
