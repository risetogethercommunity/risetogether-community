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
