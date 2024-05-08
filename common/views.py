# common/views.py

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm

def logout_view(request):
    logout(request)
    return redirect('common:login')

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('common:login')
    else:
        form = SignUpForm()
    return render(request, 'common/signup.html', {'form': form})
