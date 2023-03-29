from django.shortcuts import render
from utils.weather_api import *
from .models import dataMCU
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import SignUpForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
# Create your views here.

@login_required(login_url='login_view')
def home(request):
    mcuData = dataMCU.objects.get(user=request.user)
    Weather_API = WeatherAPI('q9iopHj6fBtlpBflx9ewLcK1arBp6Tvo', 'me')
    homeview_data = Weather_API.get_all_weather_data()
    homeview_data['soil_moisture'] = mcuData.soil_moisture
    homeview_data['soil_temperature'] = mcuData.soil_temp
    homeview_data['wind_speed'] = mcuData.wind_speed
    return render(request, 'index.html', {'homeview_data': homeview_data})

@unauthenticated_user
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            dataMCU.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')