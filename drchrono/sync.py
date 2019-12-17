from drchrono.endpoints import DoctorEndpoint, PatientEndpoint, AppointmentEndpoint
from drchrono.models import Doctor, Patient, Appointment
# from drchrono.serializers import DoctorSerializer1, PatientSerializer1, AppointmentSerializer1
# , PatientSerializer1, AppointmentSerializer1
from drchrono.serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer

from social_django.models import UserSocialAuth

from datetime import datetime, timedelta, date
from django.utils import timezone
from django.utils.timezone import now

class synchron_data():
    def __init__(self):
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        self.access_token = oauth_provider.extra_data['access_token']
        self.today = now()
        # self.today = datetime.strptime("2019-11-26", "%Y-%m-%d")
        self.one_days_ago = self.today - timedelta(days=1)
        self.one_days_after = self.today + timedelta(days=1)

    def synchron(self, Endpoint, Serializer, Model, type_name):
        endpoint = Endpoint(self.access_token)

        params = {}
        if type_name == 'appointment':
            params = {'start': self.one_days_ago, 'end' : self.one_days_after}

        endpoint_list = endpoint.list(**params)

        # print list(endpoint_list)

        for data in endpoint_list:
            # print "test"

            data = dict(data)
            print data

            try:
                model = Model.objects.get(id=data['id'])
                serializer = Serializer(model, data=data)
                
            except Model.DoesNotExist:
                serializer = Serializer(data=data)
            
            if serializer.is_valid():
                serializer.save()


def synchron_all_data():
    object_data = synchron_data()
    object_data.synchron(DoctorEndpoint, DoctorSerializer, Doctor, 'doctor')
    object_data.synchron(PatientEndpoint, PatientSerializer, Patient, 'patient')
    object_data.synchron(AppointmentEndpoint, AppointmentSerializer, Appointment, 'appointment')

    

if __name__ == '__main__':
    synchron_all_data()