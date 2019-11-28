from drchrono.endpoints import DoctorEndpoint, PatientEndpoint, AppointmentEndpoint
from drchrono.models import Doctor, Patient, Appointment
from drchrono.serializers import DoctorSerializer1, PatientSerializer1, AppointmentSerializer1
from drchrono.serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer

from social_django.models import UserSocialAuth

from datetime import datetime, timedelta, date
from django.utils import timezone

class synchron_data():
    def __init__(self):
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        self.access_token = oauth_provider.extra_data['access_token']

    def synchron(self, Endpoint, Serializer, Model, type_name):
        endpoint = Endpoint(self.access_token)

        endpoint_list = []
        if type_name == 'appointment':
            # endpoint_list = endpoint.list(start = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d'), end = datetime.strftime(datetime.now() + timedelta(1), '%Y-%m-%d'))
            today = date.today()
            # print today
            # tomorrow = date.today() + timedelta(days=1)
            # print tomorrow
            for i in range(-2, 4):
                var_date = date.today() + timedelta(days=i)

            # for d in [today, tomorrow]:
                endpoint_list += endpoint.list(date=var_date)
            # print((list(endpoint_list)))
        else:
            endpoint_list = endpoint.list()

        # print list(endpoint_list)

        for data in endpoint_list:
            # print "test"

            data = dict(data)
            # if type_name == 'appointment':
            #     print type_name, data['doctor'], data['id'], data['patient']

            # print data
            serializer = Serializer(data=data)

            if serializer.is_valid():

                try:
                    # print serializer.validated_data
                    model = Model.objects.get(id=serializer.validated_data['id'])
                    serializer.update(model, serializer.validated_data)
                
                except Model.DoesNotExist:
                    serializer.create(serializer.validated_data)

            else:
                print data

    
def synchron_all_data():
    object_data = synchron_data()
    object_data.synchron(DoctorEndpoint, DoctorSerializer1, Doctor, 'doctor')
    object_data.synchron(PatientEndpoint, PatientSerializer1, Patient, 'patient')
    object_data.synchron(AppointmentEndpoint, AppointmentSerializer1, Appointment, 'appointment')

    

if __name__ == '__main__':
    synchron_all_data()