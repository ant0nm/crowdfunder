"""crowdfunder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.root, name="root"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('projects/', views.project_page, name="project_page"),
    path('projects/<int:project_id>', views.show_project, name="show_project"),
    path('projects/new', views.create_project, name="create_project"),
    path('profile/<int:id>', views.profile, name="user_profile"),
    path('profile/create', views.profile_create, name="profile_create"),
    path('projects/<int:project_id>/rewards/create', views.reward_create, name="reward_create"),
]
