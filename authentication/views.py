from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
import smtplib, ssl
from django.contrib import auth
from django.urls import reverse

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
import configs

settings = configs.get_settings()


# Create your views here.
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error' : 'Username should only contain alphanumeric' }, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error' : 'Username already taken, try another one' }, status=409)
        return JsonResponse({'username_valid': True})
    
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error' : 'Email is invalid' }, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'The email has already been taken, try another one'}, status=409)
        return JsonResponse({'email_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        #GET USER DATA
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        context = {
            'fieldValues':request.POST
        }
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                
                if len(password)<6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                    
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                    'uidb64':uidb64,
                    'token':token_generator.make_token(user)
                })
                
                activate_url = '=http://'+domain+link
                
                
                email_subject = "Activate your accout"
                email_body='Hi ' + user.username+'.' + 'Pleae use this link to activate your account.\n' +  activate_url
                
                EMAIL_PORT = settings.email_port
                SMTP_SERVER = settings.smtp_server
                SENDER_EMAIL = settings.sender_email
                EMAIL_USER_PASSWORD = settings.email_user_password
                
                
                message = email_body

                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(SMTP_SERVER, EMAIL_PORT, context=context) as server:
                    server.login(SENDER_EMAIL, EMAIL_USER_PASSWORD)
                    server.sendmail(SENDER_EMAIL, email, message)
                
                messages.success(request, 'Account created successfully')
                return render(request, 'authentication/register.html')
            
            
class VerificationView(View):
    def get(self, request, uidb64, token):
        
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
            if not token_generator.check_token(user, token):
                messages.success(request, 'This account has alredy been activated')
                return redirect('login'+'?message='+'User already activated')
                
            
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            
            messages.success(request, 'Account activated successfully')
            return redirect('login')
            
        except Exception as e:
            pass
        
        return redirect('login')
    
                 
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username + ' you are now logged in')
                    return redirect('expenses')
    
                messages.error(request, 'Account is not activated, please check your email')
                return render(request, 'authentication/login.html')
            
            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html')
        
        messages.error(request, 'Please fill all the fields')
        return render(request, 'authentication/login.html')
    
            
    
class SetNewPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/set-newpassword.html')
    
class ResetPassword(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')
    
    
    
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out")
        return redirect('login')