from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth', views.participant_signup, name='auth'),
    path('login', views.signin, name='login'),
    path('delete_user', views.delete_data, name='delete_user'),
    path('password_reset', views.reset_password, name='password_reset'),
    path('change_info', views.change_information, name='change_info'),
    path('create_superuser', views.add_superuser, name='create_superuser'),
    path('logout', views.signout, name='logout'),
    path('landing', views.landing_view, name='landing'),
]
