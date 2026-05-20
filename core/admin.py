from django.contrib import admin
from .models import Freelancer, ClientProfile, Lead, BlogPost, Campaign

@admin.register(Freelancer)
class FreelancerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'skill', 'experience_years']

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'company', 'industry']

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['get_sender_name', 'freelancer', 'created_at']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['platform', 'is_active', 'likes', 'created_at']
