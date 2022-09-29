from datetime import datetime
from multiprocessing import context
from tabnanny import check
from django.core.paginator import Paginator
from pydoc import cli
from pyexpat import model
from re import M
from statistics import mode
from tkinter import N
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
import re
from datetime import timedelta
import pyperclip

def manualimport(request):
    context = {}
    if request.method == "POST":
        clipboard = request.POST['services']
        clipboard = clipboard.split('\n')
        records = []
        counter = 0
        for record in clipboard:
            if not record == '':
                clipboard[counter] = record.replace('\r',"").split("\t")
                if len(clipboard[counter]) == 15: #manual input from the clipboard should contain 12 values
                    try:
                        clipboard[counter][0] = int(clipboard[counter][0])
                        if not clipboard[counter][1] == '':
                            clipboard[counter][1] = 0
                        clipboard[counter][2] = str(clipboard[counter][2])
                        clipboard[counter][3] = str(clipboard[counter][3])
                        clipboard[counter][4] = todatetime(clipboard[counter][4])
                        clipboard[counter][5] = todatetime(clipboard[counter][5])
                        clipboard[counter][6] = str(clipboard[counter][6])
                        clipboard[counter][7] = str(clipboard[counter][7])
                        clipboard[counter][8] = int(clipboard[counter][8])
                        clipboard[counter][9] = int(clipboard[counter][9])
                        clipboard[counter][10] = str(clipboard[counter][10].split('E')[0])
                        clipboard[counter][11] = str(clipboard[counter][11])
                        clipboard[counter][12] = str(clipboard[counter][12])
                    except:
                        return HttpResponse("Format error. The following information does not match with an ocassional service: \n" + str(clipboard[counter][0]))
                    
                    if type(clipboard[counter][0]) == int and type(clipboard[counter][2]) == str and type(clipboard[counter][3]) == str and type(clipboard[counter][4]) == datetime and type(clipboard[counter][5]) == datetime and type(clipboard[counter][6]) == str and type(clipboard[counter][7]) == str and type(clipboard[counter][8]) == int and type(clipboard[counter][9]) == int and type(clipboard[counter][10]) == str and type(clipboard[counter][11]) == str and type(clipboard[counter][12]) == str:
                        
                        check = serviceorder.objects.filter(SO=clipboard[counter][0])
                        if check:
                            #updates existing SO information
                            check.update(name=clipboard[counter][2], customer=clipboard[counter][3], starttime=clipboard[counter][4], endtime=clipboard[counter][5], origin=clipboard[counter][6], destination=clipboard[counter][7], duration=clipboard[counter][8], extension=clipboard[counter][9], salesprice=clipboard[counter][10], traffictype=clipboard[counter][11], project=clipboard[counter][12], salesrepresentative=clipboard[counter][13], bookedby=clipboard[counter][14])

                        else:
                            new = serviceorder.objects.create(SO=clipboard[counter][0], name=clipboard[counter][2], customer=clipboard[counter][3], starttime=clipboard[counter][4], endtime=clipboard[counter][5], origin=clipboard[counter][6], destination=clipboard[counter][7], duration=clipboard[counter][8], extension=clipboard[counter][9], salesprice=clipboard[counter][10], traffictype=clipboard[counter][11], project=clipboard[counter][12], salesrepresentative=clipboard[counter][13], bookedby=clipboard[counter][14])
                            new.save()
                            servicecoordination.objects.create(SO=new)      
                else:
                    if not clipboard[counter] == '':
                        return HttpResponse("Format error. The information does not match with ocassional services information: " + record )
            counter += 1
            


        return redirect('services:services_overview')
    

    return render(request, "import.html", context)

def todatetime(string):
    return datetime.strptime(str(string).replace('.0',""),"%Y-%m-%d %H:%M:%S")

def servicesoverview(request, *args, **kwargs):
    
    
    context = {
        'services':servicecoordination.objects.filter(SO__endtime__gte=datetime.now() + timedelta(minutes=120)).exclude(SO__customer="Fanatiz").order_by('SO__starttime')    
    }
    
    return render(request, 'services.html', context)

def recalculatecoordination(request):

    services = serviceorder.objects.filter(starttime__gte=datetime.now().date())
    coordinations = servicecoordination.objects.filter(SO__starttime__gte=datetime.now().date())
    for service in services:
        check = coordinations.filter(SO_id=service.SO).first()
        if not check:
            servicecoordination.objects.create(SO=service)
    return redirect('services:services_overview')        

def savechanges_view(request): #to be improved with an API request
    if request.method == "POST":
        so = request.POST['so']
        monitor = request.POST['monitor']
        origin = request.POST['origin']
        destination = request.POST['destination']
        service = servicecoordination.objects.filter(SO_id=so)
        if not service.first().monitor == monitor and not monitor == "":
            coordinationlog.objects.create(SO_id=so, comment=str(request.user) + " changed monitoring from: " + str(service.first().monitor) + " to: " + monitor)
            service.update(monitor=monitor)
        if not service.first().origin == origin and not origin == "":
            coordinationlog.objects.create(SO_id=so, comment=str(request.user) + " changed coordination origin from: " + str(service.first().origin) + " to: " + origin)
            service.update(origin=origin)
        if not service.first().destination == destination and not destination == "":
            coordinationlog.objects.create(SO_id=so, comment=str(request.user) + " changed coordination destination from: " + str(service.first().destination) + " to: " + destination)
            service.update(destination=destination)

    return redirect('services:services_overview')


def checkbooking_view(request, so): #to be improved with an API request
    service = servicecoordination.objects.get(SO_id=so)
    if not request.user in service.checkedby.all():
        service.checkedby.add(request.user)
        service.save()
        coordinationlog.objects.create(SO_id=so, comment=str(request.user) + " checked the booking")
    return redirect('services:services_overview')

def openconnections_view(request, so): #to be improved with an API request
    service = servicecoordination.objects.get(SO_id=so)
    if not service.openedby:
        service.openedby = request.user
        service.save()
        coordinationlog.objects.create(SO_id=so, comment=str(request.user) + " opened the connection")
    return redirect('services:services_overview')

def originok_view(request, so): #to be improved with an API request
    service = servicecoordination.objects.get(SO_id=so)
    if not request.user in service.originok.all():
        service.originok.add(request.user)
        service.save()
        coordinationlog.objects.create(SO_id=so, comment=str(request.user) + " confirmed origin signal OK")
    return redirect('services:services_overview')

def destinationok_view(request, so): #to be improved with an API request
    service = servicecoordination.objects.get(SO_id=so)
    if not service.destinationok:
        service.destinationok = request.user
        service.save()
        coordinationlog.objects.create(SO_id=so, comment=str(request.user) + " confirmed destination signal OK with the client")
    return redirect('services:services_overview')

def issuereport_view(request, so):
    logs = coordinationlog.objects.filter(SO_id=so)
    issuelogs = issuereportlogs.objects.filter(SO_id=so)
    print(issuelogs)
    logsfull = []
    if logs:
        for log in logs:
            logsfull.append(log)
    if issuelogs:
        for log in issuelogs:
            logsfull.append(log)
    context = {
        'service': serviceorder.objects.get(SO=so),
        'logs': logsfull
    }
    return render(request, "issue-report.html", context)