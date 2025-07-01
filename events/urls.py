from django.urls import path
from events.views import *

urlpatterns = [
    path('',home, name='home'),
    path('dashboard/',dashboard, name='dashboard'),
    path('events/',event_list, name='event_list'),
    path('events/<int:id>/',event_detail, name='event_detail'),
    path('events/add/',event_create, name='event_create'),
    path('events/<int:id>/edit/',event_update, name='event_update'),
    path('events/<int:id>/delete/',event_delete, name='event_delete'),


]
