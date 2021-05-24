from django.urls import path

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
    path('add_service', views.add_resource, name='add_service'),
    path('view_service/<int:pk>/', views.view_resource, name='view_service'),
    path('edit_service/<int:pk>/', views.edit_resource, name='edit_service'),
    path('delete_service/<int:pk>', views.delete_resource, name='delete_service')
]
