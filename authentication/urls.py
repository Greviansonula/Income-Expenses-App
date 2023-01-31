from django.urls import path
from . views import RegistrationView, LoginView, ResetPassword, SetNewPasswordView, UsernameValidationView, EmailValidationView, VerificationView, LogoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('resetpassword', ResetPassword.as_view(), name='resetpassword'),
    path('setnewpassword', SetNewPasswordView.as_view(), name='setnewpassword'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
]
