from django.urls import path
from .views import *

app_name='customers'
urlpatterns = [
    
    path('deliveryemail/<int:so>',deliverserviceemail_view, name="deliverserviceemail"),
    
]