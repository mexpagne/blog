from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out

urlpatterns = [
    path('login/', views.ClientloginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('update/', views.update_profile, name='update_profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ajax/load-states/', views.load_states, name='ajax_load_states'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('profile/', views.profile_view, name='profile'),
    path('testify/', views.testify, name='testify'),
]

@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    msg = "Did you Sign out by mistake? Let's get you back in"
    messages.add_message(request, messages.INFO, msg)