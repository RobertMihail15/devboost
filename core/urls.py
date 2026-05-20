from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('freelancers/', views.freelancers_list, name='freelancers'),
    path('freelancers/<int:freelancer_id>/', views.freelancer_detail, name='freelancer_detail'),
    path('freelancers/<int:freelancer_id>/contact/', views.contact_freelancer, name='contact_freelancer'),
    path('blog/', views.blog, name='blog'),
    path('blog/add/', views.blog_add, name='blog_add'),
    path('blog/<int:post_id>/', views.blog_post_detail, name='blog_post'),
    path('blog/<int:post_id>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<int:post_id>/delete/', views.blog_delete, name='blog_delete'),
    path('campaigns/', views.campaigns, name='campaigns'),
    path('campaigns/add/', views.campaign_add, name='campaign_add'),
    path('campaigns/<int:campaign_id>/edit/', views.campaign_edit, name='campaign_edit'),
    path('campaigns/<int:campaign_id>/delete/', views.campaign_delete, name='campaign_delete'),
    path('admin-view/', views.admin_view, name='admin_view'),
    path('api/freelancers/', views.api_freelancers, name='api_freelancers'),
    path('api/leads/', views.api_leads, name='api_leads'),
]
