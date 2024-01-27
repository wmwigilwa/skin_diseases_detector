from django.contrib import admin

# Register your models here.
from .models import UserProfile, Disease

admin.site.register(UserProfile)
admin.site.register(Disease)
