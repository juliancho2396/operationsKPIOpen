import imp
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(serviceorder)
admin.site.register(connection)
admin.site.register(servicecoordination)
admin.site.register(coordinationlog)