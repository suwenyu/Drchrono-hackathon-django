from rest_framework import serializers
from drchrono.models import Doctor, Patient, Appointment


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
    