from django.urls import path
from .views import sign_up, sign_in, logout_view, dashboard_redirect

urlpatterns = [
    path('signup/', sign_up, name='sign-up'),
    path('signin/', sign_in, name='sign-in'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
]
