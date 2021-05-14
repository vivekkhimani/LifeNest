from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('supplier_list', views.supplier_list, name='supplier_list'),
    path('supplier_auth', views.supplier_signup, name='supplier_auth'),
    path('requester_auth', views.requester_signup, name='requester_auth'),
    path('supplier_login', views.supplier_login, name='supplier_login'),
    path('requester_login', views.requester_login, name='requester_login'),
    path('verify_phone', views.verify_phone, name='verify_phone'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('change_information', views.change_information, name='change_information'),
    path('logout', views.logout, name='logout'),
    path('delete', views.delete_data, name='delete'),
    path('404', views.fallback, name='404')
]
