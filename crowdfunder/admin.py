from django.contrib import admin
from crowdfunder.models import Profile, Project, Reward, Donation, Category, Tag, Tagging

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Reward)
admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Tagging)
