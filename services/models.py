from distutils.command.upload import upload
import imp
from statistics import mode
from unicodedata import name
from django.db import models
from authentication.models import User



class serviceorder (models.Model):
    SO = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=300, null=False)
    customer = models.CharField(max_length=200, null=True) #to make a relation in the future
    starttime = models.DateTimeField(null=False)
    endtime = models.DateTimeField(null=False)
    origin = models.CharField(max_length=100, null=True) #Future auto calculation algorithm
    destination = models.CharField(max_length=100, null=True) #Future auto calculation algorithm
    duration = models.IntegerField(null=True)
    extension = models.IntegerField(null=True)
    salesprice = models.CharField(max_length=100, null=True, default='0') # do not use
    traffictype = models.CharField(max_length=100, null=True) #future implementation
    project = models.CharField(max_length=100, null=True) #future implementation
    salesrepresentative = models.CharField(max_length=300, null=True) #to make a relation in the future
    bookedby = models.CharField(max_length=100, null=False)
    def __str__(self) -> str:
        return str(self.SO) + " - " + str(self.name)


class connection (models.Model):
    ID = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    linkedso = models.ForeignKey(to=serviceorder, on_delete=models.CASCADE)
    customer = models.CharField(max_length=200, null=True) #to make a relation in the future
    type = models.CharField(max_length=100, null=True) #to bring the actual array of connection types
    status = models.CharField(max_length=100, null=True) #to bring the actual array of statuses
    alarm = models.CharField(max_length=100, null=True)   #future implementation
    source = models.CharField(max_length=100, null=True) #future implementation
    format = models.CharField(max_length=100, null=True) #to bring the actual formats in the future
    bandwith = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    starttime = models.DateTimeField(null=True)
    endtime = models.DateTimeField(null=True)
    duration = models.IntegerField(null=True)
    warmup = models.IntegerField(null=True)
    aproxout = models.IntegerField(null=True)

class servicecoordination(models.Model):
    SO = models.ForeignKey(to=serviceorder, on_delete=models.DO_NOTHING, default=None)
    checkedby = models.ManyToManyField(to=User, blank=True, related_name="checked", default=None)
    openedby = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, related_name="opened", default=None)
    originok = models.ManyToManyField(to=User, blank=True, related_name="origin", default=None)
    destinationok = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, related_name="destionation", default=None)
    comment = models.TextField(null=True, blank=True)
    monitor = models.CharField(max_length=100, null=True, blank=True) #future implementation with relation to table of monitors
    origin = models.CharField(max_length=500, null=True, blank=True) #for manual coordination process
    destination = models.CharField(max_length=500, null=True, blank=True) #for manual coordination process
    def __str__(self) -> str:
        return str(self.SO.SO) + " " + str(self.SO.name)

class coordinationlog(models.Model):
    SO = models.ForeignKey(to=serviceorder, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=False)
    def __str__(self) -> str:
        return self.comment + " - SO#: " + str(self.SO)


class issuereportlogs(models.Model):
    SO = models.ForeignKey(to=serviceorder, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=False)
    attachment = models.ImageField(upload_to='reportattachments/')


