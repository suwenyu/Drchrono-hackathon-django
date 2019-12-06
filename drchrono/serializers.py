from rest_framework import serializers
# from rest_framework.serializers import ModelSerializer, RelatedField
from drchrono.models import Doctor, Patient, Appointment

from django.utils import timezone
from datetime import datetime, timedelta

from django.utils.dateparse import parse_datetime
from django.utils.timezone import now



class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name']

    # def to_internal_value(self, data):
    #     params = {}
    #     for field in self.fields:
    #         params[field] = data[field]
    #     return params

    # def save(self, **kwargs):
    #     validated_data = dict(
    #         list(self.validated_data.items()) +
    #         list(kwargs.items())
    #     )
    #     print self.validated_data.items(), kwargs.items()
    #     print self.instance

    #     if self.instance is not None:
    #         self.instance = self.update(self.instance, validated_data)
    #     else:
    #         self.instance = self.create(validated_data)
    #     return self.instance



class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'social_security_number', 'doctor']

    # def create(self, validated_data):
    #     doctor_id = validated_data.pop('doctor')
    #     validated_data['doctor'] = Doctor.objects.get(id=doctor_id)
    #     return Patient.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     doctor_id = validated_data.pop('doctor')
    #     validated_data['doctor'] = Doctor.objects.get(id=doctor_id)
        
    #     for field_name in self.fields:
    #         setattr(instance, field_name, validated_data[field_name])
    #     instance.save()
    #     return instance



class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'status', 'scheduled_time', 'duration', 'exam_room', 'scheduled_end_time', 'checkin_time', 'waiting_time', 'start_appointment_time']

    def judge_doctor_patient(self, validated_data):
        # print validated_data.get('doctor')
        doctor_id = validated_data.pop('doctor')
        # print doctor_id
        # print "test"

        try:
            validated_data['doctor'] = Doctor.objects.get(id=doctor_id)
            print validated_data['doctor']
        except Doctor.DoesNotExist:
            return False

        patient_id = validated_data.pop('patient')
        try:
            validated_data['patient'] = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return False

        return True

    def judge_status(self, validated_data):
        status = validated_data.get('status', None)
        validated_data['checkin_time'] = None
        validated_data['waiting_time'] = None
        validated_data['start_appointment_time'] = None

        appointment_id = validated_data.get('id', None)
        if appointment_id:

            if status == "Arrived":
                validated_data['checkin_time'] = now()

            if status == "In Session" or status == "Complete":
                app = Appointment.objects.filter(pk=appointment_id).values('checkin_time')
                if app:
                    checkin_time = app[0]['checkin_time']
                    if not checkin_time:
                        validated_data['checkin_time'] = now()
                        validated_data['waiting_time'] = 0
                        validated_data['start_appointment_time'] = now()
                    else:
                        validated_data['checkin_time'] = checkin_time
                        validated_data['waiting_time'] = round((now() - checkin_time).total_seconds()/60) 
                        validated_data['start_appointment_time'] = now()

        return validated_data

    def create(self, validated_data):
        # if self.judge_doctor_patient(validated_data):
        # doctor_id = validated_data.pop('doctor')
        # try:
        #     validated_data['doctor'] = Doctor.objects.get(pk=doctor_id)
        # except Doctor.DoesNotExist:
        #     return

        # patient_id = validated_data.pop('patient')

        # try:
        #     validated_data['patient'] = Patient.objects.get(pk=patient_id)
        # except Patient.DoesNotExist:
        #     return
        # print validated_data
        validated_data['scheduled_end_time'] = validated_data['scheduled_time'] + timedelta(minutes=validated_data['duration'])
        validated_data = self.judge_status(validated_data)

        # validated_data['scheduled_end_time'] = datetime.strptime(validated_data['scheduled_time']) + timedelta(minutes=validated_data['duration'])
        return Appointment.objects.create(**validated_data)


    def update(self, instance, validated_data):
        # print validated_data, instance

        # if self.judge_doctor_patient(validated_data):

        # validated_data['scheduled_end_time'] = validated_data['scheduled_time'] + timedelta(minutes=validated_data['duration'])
            
        validated_data['scheduled_end_time'] = validated_data['scheduled_time'] + timedelta(minutes=validated_data['duration'])
        validated_data = self.judge_status(validated_data)

        for field in self.fields:
            setattr(instance, field, validated_data[field])


        instance.save()
        return instance


# class DoctorSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     first_name = serializers.CharField(max_length=255)
#     last_name = serializers.CharField(max_length=255)
    
#     def create(self, validated_data):
#         return Doctor.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.id = validated_data.get('id', instance.id)
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)

#         instance.save()
#         return instance


    # def restore_object(self, attrs, instance=None):
    #     if instance is not None:
    #         instance.id = attrs.get('id', instance.id)
    #         instance.first_name = attrs.get('first_name', instance.first_name)
    #         instance.last_name = attrs.get('last_name', instance.last_name)

    #         return instance

    #     return Doctor(**attrs)

    

# class PatientSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     first_name = serializers.CharField(max_length=255)
#     last_name = serializers.CharField(max_length=255)
#     social_security_number = serializers.CharField(max_length=255, allow_blank=True)
#     doctor = serializers.IntegerField()

#     def create(self, validated_data):
#         doctor_id = validated_data.pop('doctor')
#         validated_data['doctor'] = Doctor.objects.get(id=doctor_id)
#         return Patient.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.id = validated_data.get('id', instance.id)
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
        
#         doctor_id = validated_data.get('doctor')
#         instance.doctor = Doctor.objects.get(id=doctor_id)

#         instance.social_security_number = validated_data.get('social_security_number', instance.social_security_number)

#         instance.save()
#         return instance

    # def restore_object(self, attrs, instance=None):
    #     if instance is None:
    #         instance = attrs.get('id', instance.id)
    #         instance.first_name = attrs.get('first_name', instance.first_name)
    #         instance.last_name = attrs.get('last_name', instance.last_name)

    #         return instance

    #     return Patient(**attrs)

# class AppointmentSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     patient = serializers.IntegerField()
#     doctor = serializers.IntegerField()
#     status = serializers.CharField(max_length=255, allow_blank=True)
#     scheduled_time = serializers.DateTimeField()
#     duration = serializers.IntegerField()
#     exam_room = serializers.IntegerField()

#     scheduled_end_time = serializers.DateTimeField(required=False)
#     checkin_time = serializers.DateTimeField(required=False)
#     waiting_time = serializers.IntegerField(required=False)
#     start_appointment_time = serializers.DateTimeField(required=False)
    
#     def judge_doctor_patient(self, validated_data):
#         doctor_id = validated_data.pop('doctor')
#         try:
#             validated_data['doctor'] = Doctor.objects.get(pk=doctor_id)
#         except Doctor.DoesNotExist:
#             return False

#         patient_id = validated_data.pop('patient')
#         try:
#             validated_data['patient'] = Patient.objects.get(pk=patient_id)
#         except Patient.DoesNotExist:
#             return False

#         return True

#     def judge_status(self, validated_data):
#         status = validated_data.get('status', None)
#         validated_data['checkin_time'] = None
#         validated_data['waiting_time'] = None
#         validated_data['start_appointment_time'] = None

#         appointment_id = validated_data.get('id', None)
#         if appointment_id:

#             if status == "Arrived":
#                 validated_data['checkin_time'] = now()

#             if status == "In Session" or status == "Complete":
#                 app = Appointment.objects.filter(pk=appointment_id).values('checkin_time')
#                 if app:
#                     checkin_time = app[0]['checkin_time']
#                     if not checkin_time:
#                         validated_data['checkin_time'] = now()
#                         validated_data['waiting_time'] = 0
#                         validated_data['start_appointment_time'] = now()
#                     else:
#                         validated_data['checkin_time'] = checkin_time
#                         validated_data['waiting_time'] = round((now() - checkin_time).total_seconds()/60) 
#                         validated_data['start_appointment_time'] = now()

#         return validated_data



#     def create(self, validated_data):
#         if self.judge_doctor_patient(validated_data):
#             validated_data['scheduled_end_time'] = validated_data['scheduled_time'] + timedelta(minutes=validated_data['duration'])
#             validated_data = self.judge_status(validated_data)

#         # validated_data['scheduled_end_time'] = datetime.strptime(validated_data['scheduled_time']) + timedelta(minutes=validated_data['duration'])
#             return Appointment.objects.create(**validated_data)


#     def update(self, instance, validated_data):
#         # print validated_data, instance

#         if self.judge_doctor_patient(validated_data):

#             validated_data['scheduled_end_time'] = validated_data['scheduled_time'] + timedelta(minutes=validated_data['duration'])
            

#             validated_data = self.judge_status(validated_data)

#             for field in self.fields:
#                 setattr(instance, field, validated_data[field])

#             # print instance
#             instance.save()
#             return instance


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

# class retrieveAppointmentSerializer(serializers.Serializer):
#     id = serializers.IntegerField()

#     status = serializers.CharField(max_length=255, allow_blank=True)
#     scheduled_time = serializers.DateTimeField()
#     duration = serializers.IntegerField()
#     exam_room = serializers.IntegerField()

#     scheduled_end_time = serializers.DateTimeField(required=False)
#     checkin_time = serializers.DateTimeField(required=False)
#     waiting_time = serializers.IntegerField(required=False)
#     start_appointment_time = serializers.DateTimeField(required=False)


#     waiting_time = serializers.SerializerMethodField()
#     patient_name = serializers.StringRelatedField(source='patient')
#     scheduled_time = serializers.DateTimeField(format='%I:%M %p')
#     scheduled_end_time = serializers.DateTimeField(format='%I:%M %p')


#     def get_waiting_time(self, obj):
#         # print obj.id, obj.start_appointment_time
#         if obj.checkin_time and not obj.start_appointment_time:
#             # print "test"
#             time = int(round((now() - obj.checkin_time).total_seconds()/60))
#             if time:
#                 return time
#             return 0
