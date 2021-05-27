from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

password_reset_patterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

authpatterns = [
    path('auth', views.participant_signup, name='auth'),
    path('login', views.signin, name='login'),
    path('logout', views.signout, name='logout'),
    path('delete_user', views.delete_data, name='delete_user'),
    path('change_password', views.update_password, name='change_password'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('landing', views.landing_view, name='landing'),
    path('add_service', views.add_resource, name='add_service'),
    path('spam_view_landing', views.report_spam_landing, name='spam_view_landing'),
    path('new_spam', views.add_new_spam, name='new_spam'),
    path('view_spam/<int:pk>/', views.expand_spam, name='view_spam'),
    path('upvote_spam_undo/<int:pk>/', views.undo_spam_upvote, name='upvote_spam_undo'),
    path('edit_profile', views.update_profile, name='edit_profile'),
    path('view_service/<int:pk>/', views.view_resource, name='view_service'),
    path('edit_service/<int:pk>/', views.edit_resource, name='edit_service'),
    path('delete_service/<int:pk>', views.delete_resource, name='delete_service'),
    path('scam_service/<int:pk>', views.scam_resource, name='scam_service'),
    path('help_service/<int:pk>', views.help_resource, name='help_service'),
    path('undo_scam_service/<int:pk>', views.undo_scam_resource, name='undo_scam_resource'),
    path('undo_help_service/<int:pk>', views.undo_help_resource, name='undo_help_service'),
] + authpatterns + password_reset_patterns
