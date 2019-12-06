from django.db import models

import datetime
from django.utils import timezone
from django.utils.timezone import now
# Add your models here

class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    social_security_number = models.CharField(max_length=20, null=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Appointment(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, null=True, blank=True)
    scheduled_time = models.DateTimeField()
    duration = models.IntegerField()
    exam_room = models.IntegerField()

    scheduled_end_time = models.DateTimeField(null=True)
    checkin_time = models.DateTimeField(null=True)
    waiting_time = models.IntegerField(null=True)
    start_appointment_time = models.DateTimeField(null=True)

    # def __str__(self):
    #     return "ID: %d, Patient: %s, Doctor: %s" %(self.id, self.patient, self.doctor)
