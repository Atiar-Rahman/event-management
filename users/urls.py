<<<<<<< HEAD
from django.urls import path
from .views import sign_up, sign_in, logout_view, dashboard_redirect

urlpatterns = [
    path('signup/', sign_up, name='sign-up'),
    path('signin/', sign_in, name='sign-in'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
]
=======

from django.urls import path
from users.views import sign_up,sign_in,user_logout
urlpatterns=[
    path('sign-up/',sign_up,name='sign-up'),
    path('sign-in/',sign_in,name='sign-in'),
    path('logout/',user_logout,name='logout')
]
>>>>>>> 93dad9d (authentication added")
