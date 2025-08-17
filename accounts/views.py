from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages

User = get_user_model()
def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']
    
        if '@' in username_or_email:
            user_obj = User.objects.filter(email = username_or_email).first()
            if user_obj:
                username = user_obj.username
            else:
                username = None
        else:
            username = username_or_email

        if username:
            user = authenticate(request, username=username, password=password)
        else:
            user = None
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'accounts/auth_page.html')

def SignUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'accounts/auth_page.html', {"show_signup": True})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'accounts/auth_page.html', {"show_signup": True})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'accounts/auth_page.html', {"show_signup": True})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'accounts/auth_page.html', {"show_signup": True})


def profile(request):
    return render(request, 'accounts/profile.html', {"user": request.user})
