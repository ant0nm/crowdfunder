from django.contrib import admin
from crowdfunder.models import Profile, Project, Reward, Donation

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Reward)
admin.site.register(Donation)
