from django.urls import path
from events.views import *

urlpatterns = [
    path('',home, name='home'),
    path('dashboard/',dashboard, name='dashboard'),
    path('no-permession',no_permession,name='no-permession'),
    path('events/',event_list, name='event_list'),
    path('events/<int:id>/',event_detail, name='event_detail'),
    path('events/add/',event_create, name='event_create'),
    path('events/<int:id>/edit/',event_update, name='event_update'),
    path('events/<int:id>/delete/',event_delete, name='event_delete'),

    path('participants/',participant_list, name='participant_list'),
    path('participants/add/',participant_create, name='participant_create'),
    path('participants/<int:id>/edit/',participant_update, name='participant_update'),
    path('participants/<int:id>/delete/',participant_delete, name='participant_delete'),

    path('categories/',category_list, name='category_list'),
    path('categories/add/',category_create, name='category_create'),
    path('categories/<int:id>/edit/',category_update, name='category_update'),
    path('categories/<int:id>/delete/',category_delete, name='category_delete'),


]
