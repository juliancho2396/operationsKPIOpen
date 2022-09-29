from django.urls import path
from .views import *

app_name='dashboard'
urlpatterns = [
    path('login/',dashboard_login, name="login"),
    path('',dashboard_main, name="main"),
]