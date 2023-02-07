from django.shortcuts import render
from .models import Ride, SharerOrder
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from users.models import Vehicle
from django.core.mail import send_mail
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

# rides = [
#     {
#         'destination': 'duke university',
#         'numberpassengers': '1',
#         'date': 'Jan 31, 2023',
#         'vehicletype': 'f1'
#     },
#     {
#         'destination': 'duke hospital',
#         'numberpassengers': '2',
#         'date': 'Jan 31, 2023'
#     }
# ]


def home(request):
    context = {
        'rides': Ride.objects.all()
    }
    return render(request, 'ride/home.html', context)

class RideOwnerListView(ListView):
    model = Ride
    template_name = 'ride/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'rides'
    ordering = ['-date']
    def get_queryset(self):
        #return Ride.objects.filter(rideOwner=self.request.user or sharer.all().filter(username=self.request.user.username)).exclude(status=Ride.STATUS.completed)
        #return Ride.objects.filter(rideOwner=self.request.user or sharer.all().filter(username=self.request.user.username)=self.request.user).exclude(status=Ride.STATUS.completed)
        result1 = Ride.objects.filter(rideOwner=self.request.user).exclude(status=Ride.STATUS.completed)
        result2 = Ride.objects.filter(sharer__username=self.request.user.username).exclude(status=Ride.STATUS.completed)
        print("result1:", result1)
        print("result2:", result2)
        # result1.union(result1, result2, all=True)
        # result = Ride.objects.filter(rideOwner=self.request.user |)
        # print("result1:", result1)
        # print("result2:", result2)
        result = result1 | result2
        print("result:", result)
        result = result.order_by('date')
        result = result.distinct()
        return result
    

class RideOwnerDetailView(DetailView):
    model = Ride


class RideOwnerCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    fields = ['destAddr', 'date', 'numPeople', 'vehicleType', 'shared', 'allowSharernum', 'maxPeople', 'specRequest']
    # success_url = ''
    def form_valid(self, form):
        form.instance.rideOwner = self.request.user
        form.instance.maxPeople = form.instance.allowSharernum + form.instance.numPeople
        return super().form_valid(form)


class RideOwnerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    fields = ['destAddr', 'date', 'numPeople', 'vehicleType', 'shared', 'allowSharernum', 'maxPeople', 'specRequest']
    # success_url = ''
    def form_valid(self, form):
        form.instance.rideOwner = self.request.user
        form.instance.maxPeople = form.instance.allowSharernum + form.instance.numPeople
        return super().form_valid(form)
    
    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.rideOwner:
            return True
        return False



def sharerdelete(request, pk):
    # context = {
    #     'rides': Ride.objects.all()
    # }
    ride = Ride.objects.filter(pk=pk).first()
    # ride.sharer = ride.sharer.all().exclude(username=request.user.username)
    #ride.sharer = ride.sharer.set().exclude(username=request.user.username)
    ride.sharer.remove(request.user)
    # share = self.request.user.orderOwner.last()
    sharerorder = SharerOrder.objects.filter(sharerride=ride, orderOwner=request.user).first()
    ride.allowSharernum += sharerorder.numPeople
    ride.save()
    sharerorder.delete()
    # messages.success(request, f'Your sharer ride hass been deleted!')
    # return render(request, 'ride/home.html')
    return redirect('ride-home')
    
    # return redirect('ride/home.html')

class RideOwnerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ride
    success_url = '/ride/'
    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.rideOwner:
            return True
        return False
    

def about(request):
    return render(request, 'ride/about.html', {'title': 'About'})


class SharerOrderCreateView(LoginRequiredMixin, CreateView):
    model = SharerOrder
    fields = ['destAddr', 'earliestDate', 'latestDate', 'numPeople' ]
    # success_url = ''
    def form_valid(self, form):
        form.instance.orderOwner = self.request.user
        return super().form_valid(form)

class SharerOrderPickListView(ListView):
    template_name = 'ride/sharerorder_list.html'
    def get_queryset(self):
        share = self.request.user.orderOwner.last()
        return Ride.objects.filter(shared=True,
            destAddr=share.destAddr,
            status=Ride.STATUS.opened,
            date__gte=share.earliestDate,
            date__lte=share.latestDate,
            allowSharernum__gte=share.numPeople).exclude(rideOwner=self.request.user).exclude(sharer__in=[self.request.user]).order_by('date')




def sharerjoin(request, pk):
    ride = Ride.objects.filter(pk=pk).last()
    print("request user:", request.user)
    print("ride:", ride.destAddr)
    # shareorder = SharerOrder.objects.filter(orderOwner=request.user.id).first()
    shareorder = SharerOrder.objects.filter(orderOwner=request.user).last()
    print("shareorder destAddr, numPepople:", shareorder.destAddr, shareorder.numPeople)
    ride.sharer.add(request.user)
    print('current allowSharenum', ride.allowSharernum)
    ride.allowSharernum = ride.allowSharernum - shareorder.numPeople
    print('shareorder.numPeople', shareorder.numPeople)
    print('current allowSharenum', ride.allowSharernum)
    shareorder.sharerride = ride
    ride.save()
    print("shareorder will save")
    shareorder.save()
    print("shareorder after save")
    # return render(request, 'ride/home.html')
    return redirect('ride-home')



# def sharersearch(request):
#     model = Ride
#     fields = ['']

# for search
class DriverSearchListView(ListView):
    model = Ride
    template_name = 'ride/driversearch_list.html'  # <app>/<model>_<viewtype>.html
    # context_object_name = 'rides'
    # ordering = ['-date']
    def get_queryset(self):
        vehicle = Vehicle.objects.filter(owner=self.request.user).first()
        return Ride.objects.filter(status=Ride.STATUS.opened,
        maxPeople__lte=vehicle.capacity,
        vehicleType__in=['--', vehicle.vehicle_type],
        specRequest__in=['', vehicle.special_info]).exclude(rideOwner=self.request.user).order_by('date')

# for view current
class DriverListView(ListView):
    model = Ride
    template_name = 'ride/driver_list.html'  # <app>/<model>_<viewtype>.html
    # context_object_name = 'rides'
    # ordering = ['-date']
    def get_queryset(self):
        vehicle = Vehicle.objects.filter(owner=self.request.user).first()
        return Ride.objects.filter(status=Ride.STATUS.confirmed,
            driver=self.request.user).order_by('date')



def confirm(request, pk):
    ride = Ride.objects.filter(pk=pk).first()
    # vehicle = Vehicle.objects.filter(rideOwner=request.user).first()
    ride.status = Ride.STATUS.confirmed
    ride.driver = request.user
    ride.save()
    #send eamil to rideowner
    send_mail(
        'Welcome to ridesharingservice',
        'As a ride-owner, your ride has been comfirmed',
        'ridesharingservice1@gmail.com',
        [ride.rideOwner.email],
        fail_silently=False,
    )
    print("ride", ride)
    sharers = ride.sharerride.all()
    print("sharers set", sharers)
    for sharer in sharers:
        send_mail(
        'Welcome to ridesharingservice',
        'As a ride-sharer, your ride has been comfirmed',
        'ridesharingservice1@gmail.com',
        [sharer.orderOwner.email],
        fail_silently=False,
        )
        print("send eamil to sharer")
    # return render(request, 'ride/home.html')
    return redirect('ride-home')


def complete(request, pk):
    ride = Ride.objects.filter(pk=pk).first()
    ride.status = Ride.STATUS.completed
    ride.save()
    # return render(request, 'ride/home.html')
    return redirect('ride-home')


