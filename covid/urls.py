from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('resource_list', views.resource_list, name='resource_list'),
    path('auth', views.suppliers, name='auth'),
    path('logout', views.logout, name='logout'),
    path('delete', views.delete_data, name='delete'),
    path('404', views.fallback, name='404')
]
