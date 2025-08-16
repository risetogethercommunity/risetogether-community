from django.shortcuts import render
from django.contrib.auth import authenticate, login

def user_login(request):
    return render(request, 'accounts/auth_page.html')
