from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages



from django.shortcuts import render
from .models import CustomUser

def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'myapp/user_list.html', {'users': users})




def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful. You can now log in.")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = SignupForm()
    return render(request, 'myapp/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('fatch')  # Redirect to the home page after successful login
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html', {'form': form})



@login_required
def index(request):
    email = request.user.email if request.user.is_authenticated else None
    id = request.user.id if request.user.is_authenticated else None
    print(id)
    

    return render(request, 'myapp/index.html', {'email': email} )

def user_logout(request):
    logout(request)
    return redirect('login')