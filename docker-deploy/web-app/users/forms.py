from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Vehicle
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']
        # fields = ['email']

# class VehicleCreateForm(forms.ModelForm):
#     class Meta:
#         model = Vehicle
#         fields = ['owner', 'license_number', 'capacity', 'vehicle_type', 'special_info']

class VehicleUpdateForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_number', 'capacity', 'vehicle_type', 'special_info']

