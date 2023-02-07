from django.urls import path
from .views import (
    RideOwnerListView, 
    RideOwnerDetailView,
    RideOwnerCreateView,
    RideOwnerUpdateView,
    RideOwnerDeleteView,
)
from . import views

#app_name = 'polls'
urlpatterns = [
    # ex: /
    path('', views.home, name='home'),
    path('ride/', RideOwnerListView.as_view(), name='ride-home'),
    path('ride/<int:pk>/', RideOwnerDetailView.as_view(), name='ride-detail'),
    path('ride/new/', RideOwnerCreateView.as_view(), name='ride-create'),
    path('ride/<int:pk>/update/', RideOwnerUpdateView.as_view(), name='ride-update'),
    path('ride/<int:pk>/delete/', RideOwnerDeleteView.as_view(), name='ride-delete'),
    path('ride/<int:pk>/sharerdelete/', views.sharerdelete, name='sharer-delete'),
    # ex: /about/
    path('about/', views.about, name='ride-about'),

    path('ridesharer/new/', views.SharerOrderCreateView.as_view(), name='sharerorder-create'),
    path('ridesharer/listview/', views.SharerOrderPickListView.as_view(), name='sharerorder-list'),
    path('ridesharer/<int:pk>/', views.sharerjoin, name='sharer-join'),
    #path('rideowner/', RideListView.as_view(), )

    path('driver/searchlistview/', views.DriverSearchListView.as_view(), name='driver-search'),
    path('driver/listview/', views.DriverListView.as_view(), name='driver-list'),
    path('driver/<int:pk>/confirm', views.confirm, name='driver-confirm'),
    path('driver/<int:pk>/complete', views.complete, name='driver-complete'),
    # # ex: /polls/
    # path('', views.IndexView.as_view(), name='index'),
    # # path('', views.index, name='index'),
    # # ex: /polls/5/
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # # path('<int:question_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]