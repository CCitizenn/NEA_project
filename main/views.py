from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

def loginCustomer(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")  # automatically move to homepage after login
            else:
                form.add_error(None, "Invalid username or password.") 
    else:
        form = LoginForm()
    return render(request, "login/login.html", {"form": form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # after registering, auto-login
            return redirect('/')  
    else:
        form = RegisterForm()
    return render(request, "login/register.html", {"form": form})

def login_view(request): #this is for seeing any future bookings by logging into the account
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("user_bookings") 
        else:
            return render(request, "login/login.html", {"error": "Invalid email or password"})

    return render(request, "login/login.html")

# for logging out in the staffpanel sidebar (and maybe others)
def custom_logout(request):
    logout(request)
    return redirect('/')