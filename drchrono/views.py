from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from social_django.models import UserSocialAuth

from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseNotFound

from drchrono.endpoints import DoctorEndpoint, AppointmentEndpoint, PatientEndpoint
from drchrono.models import Appointment, Patient, Doctor
from drchrono.serializers import AppointmentSerializer, retrieveAppointmentSerializer
from drchrono.forms import checkin_form, patient_info_form

from drchrono.sync import synchron_all_data

from datetime import datetime, timedelta
from django.utils.timezone import now

from django.db import models

def login(request):
    if request.user.is_authenticated():
        return redirect('index')

    return render(request, 'kiosk_setup.html')


@login_required(login_url='/login')
def synchron_db(request):
    synchron_all_data()
    print "Sync everything, then redirect back to the today screen"
    return redirect('index')


@login_required(login_url='/login')
def index(request):

    oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
    access_token = oauth_provider.extra_data['access_token']

    api = DoctorEndpoint(access_token)
    doctor = next(api.list())
    request.session['doctor'] = doctor['id']

    context = {}
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today = datetime.strptime("2019-11-27", "%Y-%m-%d")
    tomorrow = today + timedelta(days=1)
    # print today, tomorrow

    queryset = Appointment.objects.filter(
        scheduled_time__gte=today,
        scheduled_time__lte=tomorrow,
        doctor=doctor['id']
    ).order_by('scheduled_time')

    serializer_class = retrieveAppointmentSerializer(queryset, many=True)
    context['appointments'] = serializer_class.data

    wait_time = Appointment.objects.filter(
        scheduled_time__gte=today,
        scheduled_time__lte=tomorrow,
        doctor=doctor['id'],
        waiting_time__isnull=False
    ).aggregate(models.Avg('waiting_time'))['waiting_time__avg']
    context['wait_time'] = wait_time

    context['current_time'] = now()

    return render(request, 'index.html', context)
        
@login_required(login_url='/login')
def checkin(request):

    form = checkin_form(request.POST or None)
    if form.is_valid():
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today = datetime.strptime("2019-11-27", "%Y-%m-%d")
        tomorrow = today + timedelta(days=1)

        # print form
        params = {}
        for field in form.cleaned_data:
            if form.cleaned_data.get(field) == "":
                continue
            params[field] = form.cleaned_data.get(field)
        

        filters = {"{}".format(field): params[field] for field in params}
        try:
            patient = Patient.objects.get(**filters)
        except Patient.DoesNotExist:
            res = {}
            res['checkin_form'] = form
            res['message'] = 'No Patient found'
            return render(request, 'checkin.html', res)
        except Patient.MultipleObjectsReturned:
            res = {}
            res['checkin_form'] = form
            res['message'] = 'Multiple Account found'
            return render(request, 'checkin.html', res)
            
        patient = Patient.objects.filter(**filters).values()
        appointments = Appointment.objects.filter(
            doctor=request.session['doctor'],
            patient=patient[0]['id'], 
            scheduled_time__gte=today, 
            scheduled_time__lte=tomorrow
        ).order_by('scheduled_time').values()

        return render(request, 'confirm_appointment.html', {"appointments": appointments, "patient":patient[0]})
    # for i in check_form.base_fields:
    #     print i

    return render(request, "checkin.html", {'checkin_form': form})


@login_required(login_url='/login')
def comfirmcheckin(request):
    
    if request.method == 'POST':

        appointment_id = request.POST.get('appointment', None)
        # appointment_id = request.GET.get('appointment', None)
        # print appointment_id

        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        endpoint = AppointmentEndpoint(access_token)

        res = endpoint.update(appointment_id, {'status': 'Arrived'})
        if res:
            message = 'Sorry, fail to check in.'
            return HttpResponse(message, status=403) 


        api_data = endpoint.fetch(id=appointment_id)
        serializer = AppointmentSerializer(data=api_data)
    
        if serializer.is_valid():
            # print serializer.data
            # print serializer.data
            model = Appointment.objects.get(pk=serializer.validated_data['id'])
            serializer.update(model, serializer.validated_data)

        

        params = {'checkin_time' : now()}
        Appointment.objects.filter(pk=appointment_id).update(**params)
        
        message = 'Successfully check in.'
        return HttpResponse(message, status=200)
    
    # return render(request, 'checkin_success.html')

    message = 'Sorry, fail to check in.'
    return HttpResponse(message, status=403)


@login_required(login_url='/login')
def startAppointments(request, appointment):
    appointment_id = appointment
    status = 'In Session'
    
    oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
    access_token = oauth_provider.extra_data['access_token']
    endpoint = AppointmentEndpoint(access_token)
    endpoint.update(appointment_id, {'status':status})
    api_data = endpoint.fetch(id=appointment_id)

    serializer = AppointmentSerializer(data=api_data)
    
    if serializer.is_valid():
        # print serializer.data
        # print serializer.data
        model = Appointment.objects.get(pk=serializer.validated_data['id'])
        serializer.update(model, serializer.validated_data)
        #


    app = Appointment.objects.filter(pk=appointment_id).values('checkin_time')
    checkin_time = app[0]['checkin_time'] if app[0]['checkin_time'] != None else now()

    params = {'start_appointment_time': now(), 'waiting_time' : round((now() - checkin_time).total_seconds()/60) }
    Appointment.objects.filter(pk=appointment_id).update(**params)

        # waiting = (now - app_check_time[0]['checkin_time']).to_seconds()/60
        # Appointment.objects.filter(id=appointment_id).update(waiting_time=waiting, start_appointment_time=now)

    return redirect('index')

@login_required(login_url='/login')
def finishAppointments(request, appointment):
    appointment_id = appointment
    status = 'Complete'
    
    oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
    access_token = oauth_provider.extra_data['access_token']
    endpoint = AppointmentEndpoint(access_token)
    endpoint.update(appointment_id, {'status':status})
    api_data = endpoint.fetch(id=appointment_id)

    serializer = AppointmentSerializer(data=api_data)
    if serializer.is_valid():
        model = Appointment.objects.get(pk=serializer.validated_data['id'])
        serializer.update(model, serializer.validated_data)

    # Appointment.objects.filter(pk=appointment_id).update(**params)

    return redirect('index')
    

@login_required(login_url='/login')
def cancelAppointments(request, appointment):
    appointment_id = appointment
    status = 'Cancelled'
    
    oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
    access_token = oauth_provider.extra_data['access_token']
    endpoint = AppointmentEndpoint(access_token)
    endpoint.update(appointment_id, {'status':status})
    api_data = endpoint.fetch(id=appointment_id)

    serializer = AppointmentSerializer(data=api_data)
    if serializer.is_valid():
        model = Appointment.objects.get(pk=serializer.validated_data['id'])
        serializer.update(model, serializer.validated_data)

    return redirect('index')


@login_required(login_url='/login')
def update_patient_info(request, patient):
    patient_id = patient

    oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
    access_token = oauth_provider.extra_data['access_token']

    patient = Patient.objects.filter(pk=patient_id).values()[0]
    endpoint = PatientEndpoint(access_token)
    api = endpoint.fetch(id=patient_id)

    if request.POST:
        form = patient_info_form(request.POST)
    else:
        form = patient_info_form(initial=api)

    if form.is_valid():

        params = {}
        for field in form.cleaned_data:
            if form.cleaned_data[field] != "" and form.cleaned_data[field] != None:
                params[field] = form.cleaned_data[field]

        print params
        endpoint.update(patient_id, params)

        return redirect('index')
    
    return render(request, 'patient_info.html', {'form' : form, 'patient' : patient })


@login_required(login_url='/login')
def logout(request):
    django_logout(request)
    return redirect('login')


@login_required(login_url='/login')
def test1(request):
    oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
    access_token = oauth_provider.extra_data['access_token']

    endpoint = PatientEndpoint(access_token)
    print next(endpoint.list())
    # queryset = Appointment.objects.all()

    # serializer_class = retrieveAppointmentSerializer(queryset, many=True)
    # content = serializer_class.data
    # print content
    return render(request, 'debug.html', {'data': next(endpoint.list())})

@login_required(login_url='/login')
def test(request):
    
    appointment_id = "134913622"
    oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
    access_token = oauth_provider.extra_data['access_token']
    endpoint = AppointmentEndpoint(access_token)
    endpoint.update(appointment_id, {'status': "Arrived"})
    api_data = endpoint.fetch(id=appointment_id)
    print api_data

    return render(request, 'doctor_welcome.html', {"appointments": api_data })


# class SetupView(TemplateView):
#     """
#     The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
#     """
#     template_name = 'kiosk_setup.html'


# class DoctorWelcome(TemplateView):
#     """
#     The doctor can see what appointments they have today.
#     """
#     template_name = 'doctor_welcome.html'

#     def get_token(self):
#         """
#         Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
#         already signed in.
#         """
#         oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
#         access_token = oauth_provider.extra_data['access_token']
#         return access_token

#     def make_api_request(self):
#         """
#         Use the token we have stored in the DB to make an API request and get doctor details. If this succeeds, we've
#         proved that the OAuth setup is working
#         """
#         # We can create an instance of an endpoint resource class, and use it to fetch details
#         access_token = self.get_token()
#         api = DoctorEndpoint(access_token)
#         # Grab the first doctor from the list; normally this would be the whole practice group, but your hackathon
#         # account probably only has one doctor in it.
#         return next(api.list())

#     def get_context_data(self, **kwargs):
#         kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
#         # Hit the API using one of the endpoints just to prove that we can
#         # If this works, then your oAuth setup is working correctly.
#         doctor_details = self.make_api_request()
#         kwargs['doctor'] = doctor_details
#         return kwargs

# class TestAppointment(TemplateView):
#     template_name = 'test_appointments.html'

#     def get_token(self):
#         """
#         Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
#         already signed in.
#         """
#         oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
#         access_token = oauth_provider.extra_data['access_token']
#         return access_token

#     def make_api_request(self):
#         """
#         Use the token we have stored in the DB to make an API request and get doctor details. If this succeeds, we've
#         proved that the OAuth setup is working
#         """
#         # We can create an instance of an endpoint resource class, and use it to fetch details
#         access_token = self.get_token()
#         api = AppointmentEndpoint(access_token)
#         # Grab the first doctor from the list; normally this would be the whole practice group, but your hackathon
#         # account probably only has one doctor in it.
#         return next(api.list(date="2019-11-22"))

#     def get_context_data(self, **kwargs):
#         kwargs = super(TestAppointment, self).get_context_data(**kwargs)
#         # Hit the API using one of the endpoints just to prove that we can
#         # If this works, then your oAuth setup is working correctly.
#         appointments_details = self.make_api_request()
#         kwargs['appointments'] = appointments_details
#         return kwargs
