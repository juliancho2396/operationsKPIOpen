from django.urls import path
from .views import *

app_name='services'
urlpatterns = [
    path('import/', manualimport, name="importmanual"),
    path('',servicesoverview, name="services_overview"),
    path('refresh/', recalculatecoordination, name="refresh"),
    path('savechanges/', savechanges_view, name="savechanges"),
    path('checkbooking/<int:so>', checkbooking_view, name="checkbooking"),
    path('openconnections/<int:so>', openconnections_view, name="openconnections"),
    path('originok/<int:so>', originok_view, name="originok"),
    path('destinationok/<int:so>', destinationok_view, name="destinationok"),
    path('<int:so>/issuereport', issuereport_view, name="issuereport"),
    
]