from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages

def login_page(request):
    if request.method == 'POST' :
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid() :
            user = form.get_user()
            login(request,user)
            if user.is_superuser:
                messages.success(request,'Welcome Admin!')
                return redirect('userAdmin:dashboard')   # Admin Dashboard
            else:
                messages.success(request,'Welcome Staff!')
                return redirect('userStaff:staffDashboard')
        else:
            # Invalid login
            messages.error(request, "Invalid username or password")
    else :
        form = AuthenticationForm()
    return render(request, "login_page.html", {'form': form})

def home_redirect(request) :
    return redirect('login')

def logout_view(request):
    logout(request)
    messages.info(request, 'Logged Out!')
    return redirect('home')