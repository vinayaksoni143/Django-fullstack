from django.urls import path

from . import views

from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('register', views.register, name='register'),

    # Email verification urls

    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),

    path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),

    path('email-verification-success/<str:unique_id>/', views.email_verification_success, name='email-verification-success'),

    path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),

    # Login logout urls

    path('user-login', views.user_login, name='user-login'),

    path('user-logout', views.user_logout, name='user-logout'),

    # Dashboard

    path('dashboard', views.dashboard, name = 'dashboard'),

    path('update-account', views.update_account, name='update-account'),

    path('delete-account', views.delete_account, name='delete-account'),

    # Password management urls/views

    # 1> Submit email form
    path('reset-password', auth_views.PasswordResetView.as_view(template_name='account/password/password-reset.html'), name='reset_password'),

    # 2> Success message email was sent
    path('reset-password-sent', auth_views.PasswordResetDoneView.as_view(template_name='account/password/password-reset-sent.html'), name='password_reset_done'),

    # 3> Password reset link
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password/password-reset-form.html'), name='password_reset_confirm'),

    # 4> Success message password reset
    path('reset-password-complete', auth_views.PasswordResetCompleteView.as_view(template_name='account/password/password-reset-complete.html'), name='password_reset_complete'),

    # Shipping management
    path('manage-shipping', views.manage_shipping, name='manage-shipping'),

    
]
