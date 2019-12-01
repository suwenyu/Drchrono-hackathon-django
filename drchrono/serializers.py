from rest_framework import serializers
# from rest_framework.serializers import ModelSerializer, RelatedField
from drchrono.models import Doctor, Patient, Appointment

from django.utils import timezone
from datetime import datetime, timedelta

from django.utils.dateparse import parse_datetime
from django.utils.timezone import now

class specifiedColumn(serializers.ModelSerializer):

    def to_internal_value(self, data):

        # internal_data = {k: data.get(k, None) for k in self.fields}
        internal_data = {}
        for k in self.fields:
            if k in data:
                internal_data[k] = data[k]     
        # for k in list(internal_data.keys()):
        #     # the API gives us naive datetimes; assume they are in the local time of this kiosk.
        #     # Side note: this is a pretty big design problem for the API system now, without an easy fix.
        #     if isinstance(internal_data[k], dt.datetime) and internal_data[k].tzinfo is None:
        #         dt_aware = timezone.make_aware(internal_data[k], timezone.get_current_timezone())
        #         internal_data[k] = dt_aware
        return internal_data

class DoctorSerializer(specifiedColumn):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name']

class PatientSerializer(specifiedColumn):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'social_security_number']

class AppointmentSerializer(specifiedColumn):
    # scheduled_end_time = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'status', 'scheduled_time', 'duration', 'exam_room', 'scheduled_end_time']

    # def scheduled_end_time(self, obj):
    #     return obj.scheduled_time + timedelta(minutes=obj.duration)

    def create(self, validated_data):
        doctor_id = validated_data.pop('doctor')
        try:
            validated_data['doctor'] = Doctor.objects.get(pk=doctor_id)
            print Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            pass

        patient_id = validated_data.pop('patient')

        try:
            validated_data['patient'] = Patient.objects.get(pk=patient_id)
            print Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            print "Test"
            return

        validated_data['scheduled_end_time'] = parse_datetime(validated_data['scheduled_time']) + timedelta(minutes=validated_data['duration'])
        # validated_data['scheduled_end_time'] = datetime.strptime(validated_data['scheduled_time']) + timedelta(minutes=validated_data['duration'])
        return Appointment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        doctor_id = validated_data.pop('doctor')
        try:
            validated_data['doctor'] = Doctor.objects.get(pk=doctor_id)
            print Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return

        patient_id = validated_data.pop('patient')

        try:
            validated_data['patient'] = Patient.objects.get(pk=patient_id)
            print Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            print "Test"
            return

        
        validated_data['scheduled_end_time'] = parse_datetime(validated_data['scheduled_time']) + timedelta(minutes=validated_data['duration'])
        # Only works because the model is so simple.
        for field_name in self.fields:
            setattr(instance, field_name, validated_data[field_name])
        
        instance.save()
        return instance

    def save(self, **kwargs):
        # Dirty hack to ensure that save() will update instances if they exist
        try:
            id = self.validated_data['id']
            model = self.__class__.Meta.model
            self.instance = model.objects.get(id=id)
        except self.Meta.model.DoesNotExist:
            pass
        super(AppointmentSerializer, self).save(**kwargs)


class DoctorSerializer1(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    
    def create(self, validated_data):
        return Doctor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()
        return instance


    # def restore_object(self, attrs, instance=None):
    #     if instance is not None:
    #         instance.id = attrs.get('id', instance.id)
    #         instance.first_name = attrs.get('first_name', instance.first_name)
    #         instance.last_name = attrs.get('last_name', instance.last_name)

    #         return instance

    #     return Doctor(**attrs)

    

class PatientSerializer1(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    social_security_number = serializers.CharField(max_length=255, allow_blank=True)

    def create(self, validated_data):
        return Patient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.social_security_number = validated_data.get('social_security_number', instance.social_security_number)

        instance.save()
        return instance

    # def restore_object(self, attrs, instance=None):
    #     if instance is None:
    #         instance = attrs.get('id', instance.id)
    #         instance.first_name = attrs.get('first_name', instance.first_name)
    #         instance.last_name = attrs.get('last_name', instance.last_name)

    #         return instance

    #     return Patient(**attrs)

class AppointmentSerializer1(serializers.Serializer):
    id = serializers.IntegerField()
    patient = serializers.IntegerField()
    doctor = serializers.IntegerField()
    status = serializers.CharField(max_length=255, allow_blank=True)
    scheduled_time = serializers.DateTimeField()
    duration = serializers.IntegerField()
    exam_room = serializers.IntegerField()

    scheduled_end_time = serializers.DateTimeField(required=False)
    

    def create(self, validated_data):
        doctor_id = validated_data.pop('doctor')
        try:
            validated_data['doctor'] = Doctor.objects.get(pk=doctor_id)
        except Doctor.DoesNotExist:
            return

        patient_id = validated_data.pop('patient')

        try:
            validated_data['patient'] = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return

        validated_data['scheduled_end_time'] = validated_data['scheduled_time'] + timedelta(minutes=validated_data['duration'])

        # validated_data['scheduled_end_time'] = datetime.strptime(validated_data['scheduled_time']) + timedelta(minutes=validated_data['duration'])
        return Appointment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        doctor_id = validated_data.pop('doctor')
        try:
            validated_data['doctor'] = Doctor.objects.get(pk=doctor_id) 
        except Doctor.DoesNotExist:
            return

        patient_id = validated_data.pop('patient')

        try:
            validated_data['patient'] = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return

        
        validated_data['scheduled_end_time'] = validated_data['scheduled_time'] + timedelta(minutes=validated_data['duration'])
        for field_name in self.fields:
            setattr(instance, field_name, validated_data[field_name])
        
        # print instance
        instance.save()
        return instance





class retrieveAppointmentSerializer(serializers.ModelSerializer):
    waiting_time = serializers.SerializerMethodField()
    patient_name = serializers.StringRelatedField(source='patient')
    scheduled_time = serializers.DateTimeField(format='%I:%M %p')
    scheduled_end_time = serializers.DateTimeField(format='%I:%M %p')

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'status', 'scheduled_time', 'duration', 'exam_room', 'scheduled_end_time', 'checkin_time', 'waiting_time', 'patient_name', 'start_appointment_time']

    def get_waiting_time(self, obj):
        # print obj.id, obj.start_appointment_time
        if obj.checkin_time and not obj.start_appointment_time:
            # print "test"
            time = int(round((now() - obj.checkin_time).total_seconds()/60))
            if time:
                return time
            return 0
