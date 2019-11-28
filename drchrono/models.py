from django.db import models

import datetime
from django.utils import timezone
from django.utils.timezone import now
# Add your models here

class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(editable=False, max_length=255)
    last_name = models.CharField(editable=False, max_length=255)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(editable=False, max_length=255)
    last_name = models.CharField(editable=False, max_length=255)
    social_security_number = models.CharField(max_length=20, null=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Appointment(models.Model):
    id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, editable=False)  # Breaks have a null patient field
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, editable=False)
    status = models.CharField(max_length=255, null=True)
    scheduled_time = models.DateTimeField(editable=False)


