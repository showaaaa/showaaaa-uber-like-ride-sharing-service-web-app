from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, VehicleUpdateForm
from .models import Vehicle
from django.core.mail import send_mail

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def driver_info(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # v_form = VehicleUpdateForm(request.POST, instance=request.user.vehicle)
        # u_form = UserUpdateForm(request.POST)
        v_form = VehicleUpdateForm(request.POST)
        if u_form.is_valid() and v_form.is_valid():
            data = request.POST
            license_number = data.get('license_number')
            capacity = data.get('capacity')
            vehicle_type = data.get('vehicle_type')
            special_info = data.get('special_info')
            # update
            if(hasattr(request.user, 'vehicle')):
                vehicle = request.user.vehicle
                vehicle.license_number = license_number
                vehicle.capacity = capacity
                vehicle.vehicle_type  = vehicle_type 
                vehicle.special_info = special_info
            else:
                vehicle = Vehicle(owner=request.user, license_number=license_number, capacity = capacity, vehicle_type = vehicle_type, special_info = special_info)
            u_form.save()
            # v_form.save()
            vehicle.save()
            messages.success(request, f'Your Personal and Vehicle Info has been updated!')
            return redirect('driver_info')
    else:
        u_form = UserUpdateForm(instance=request.user)
        if(hasattr(request.user, 'vehicle')):
            v_form = VehicleUpdateForm(instance=request.user.vehicle)
        else:
            v_form = VehicleUpdateForm()

    context = {
        'u_form': u_form,
        'v_form': v_form
    }
    return render(request, 'users/driver_info.html', context)

@login_required
def removereiver(request):
    request.user.vehicle.delete()
    messages.success(request, f'Your are not a driver now!')
    return redirect('ride-home')

