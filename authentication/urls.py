import imp
from django.urls import path, include
from .views import *

app_name="authentication"

urlpatterns = [
    path('logout/',logout_view, name="logout"),
]
