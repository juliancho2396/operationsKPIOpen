import email
from operator import mod
from statistics import mode
from django.db import models

# Create your models here.
class customer(models.Model):
    cc = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(null=True, blank=True)
    nickname = models.CharField(max_length=50, null=False, blank=False)


class deliveryemails(models.Model):
    customer = models.ForeignKey(to=customer, on_delete=models.CASCADE)
    email = models.EmailField(null=False, blank=False)
    active = models.BooleanField(default=True)
    def __str__(self) -> str:
        return str(self.email)