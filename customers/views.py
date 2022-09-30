from pydoc import render_doc
from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from services.models import serviceorder
from django.core.mail import send_mail
from django.template.loader import get_template
from services.models import *
from .models import *
# Create your views here.

def deliverserviceemail_view(request, so):
    service = servicecoordination.objects.get(SO_id=so)
    emails = deliveryemails.objects.filter(customer__description=service.SO.customer)
    if len(emails) > 0:
        message = get_template('email/delivering.txt')
        html_message = get_template('email/delivering.html')
        context = {
            'service': service,
            'nickname': emails.first().customer.nickname
        }
        recipients = ['nmc@aldea.tv']
        for email in emails:
            recipients.append(email.email)
        send_mail(
            subject="SO " + str(service.SO.SO) + " " + str(service.SO.name),
            message=message.render(context),
            html_message=html_message.render(context),
            from_email='nmc@aldea.tv',
            recipient_list=recipients,
            fail_silently=False,
        )
        return redirect('services:services_overview')
    else:
        return HttpResponse("There is not any customer email registered on NMC Manager for the client " + str(service.SO.customer))
