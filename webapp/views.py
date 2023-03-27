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
from django.contrib.auth.models import Group
# Create your views here.

@login_required(login_url='login_view')
def home(request):
    orders = request.user.customer.order_set.all()
    Weather_API = WeatherAPI('q9iopHj6fBtlpBflx9ewLcK1arBp6Tvo', 'me')
    homeview_data = Weather_API.get_all_weather_data()
    dataMCU_model = dataMCU.objects.all()
    homeview_data['soil_moisture'] = dataMCU_model[0].soil_moisture
    homeview_data['soil_temperature'] = dataMCU_model[0].soil_temp
    homeview_data['wind_speed'] = dataMCU_model[0].wind_speed
    homeview_data['orders'] = orders
    return render(request, 'index.html', {'homeview_data': homeview_data})

@unauthenticated_user
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customers')
            user.groups.add(group)
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