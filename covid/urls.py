from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('supplier_list', views.supplier_list, name='supplier_list'),
    path('supplier_auth', views.supplier_signup, name='supplier_auth'),
    path('requester_auth', views.requester_signup, name='requester_auth'),
    path('volunteer_auth', views.volunteer_signup, name='volunteer_auth'),
    path('logout', views.logout, name='logout'),
    path('delete', views.delete_data, name='delete'),
    path('404', views.fallback, name='404')
]
