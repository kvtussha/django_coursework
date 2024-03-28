from django.contrib.auth.views import LoginView
from django.urls import path, include

from users.views import (RegisterView, ProfileView, ConfirmRegister, CustomLogoutView, UserPasswordResetView,
                         UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView, )

app_name = 'users'

urlpatterns = [
    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/confirm/', ConfirmRegister.as_view(), name='confirm_register'),
]
