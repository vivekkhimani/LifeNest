from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('supplier_list', views.supplier_list, name='supplier_list'),
    path('supplier_auth', views.supplier_signup, name='supplier_auth'),
    path('requester_auth', views.requester_signup, name='requester_auth'),
    path('supplier_login', views.supplier_signin, name='supplier_login'),
    path('requester_login', views.requester_signin, name='requester_login'),
    path('phone_auth', TemplateView.as_view(template_name='covid/auth.html'), name='phone_auth'),
    path('verify_phone', views.verify_phone_number, name='verify_phone'),
    path('password_reset', views.reset_password, name='password_reset'),
    path('change_info', views.change_information, name='change_info'),
    path('logout', views.signout, name='logout'),
    path('delete', views.delete_data, name='delete'),
    path('404', views.fallback, name='404')
]
