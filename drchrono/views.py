from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from social_django.models import UserSocialAuth

from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseNotFound

from drchrono.endpoints import DoctorEndpoint, AppointmentEndpoint, PatientEndpoint
from drchrono.models import Appointment, Patient, Doctor
from drchrono.serializers import AppointmentSerializer1
from drchrono.forms import checkin_form, patient_info_form

from drchrono.sync import synchron_all_data

from datetime import datetime, timedelta
from django.utils.timezone import now

from django.db import models


@login_required(login_url='/login')
def synchron_db(request):
    synchron_all_data()
    return redirect('index')

@login_required(login_url='/login')
def logout(request):
    django_logout(request)
    return redirect('login')


@login_required(login_url='/login')
def index(request):

    oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
    access_token = oauth_provider.extra_data['access_token']

    context = {}
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # today = datetime.strptime("2019-11-24", "%Y-%m-%d")
    tomorrow = today + timedelta(days=1)
    # print today, tomorrow

    queryset = Appointment.objects.filter(
        scheduled_time__gte=today,
        scheduled_time__lte=tomorrow,
    ).order_by('scheduled_time')

    serializer_class = retrieveAppointmentSerializer(queryset, many=True)
    context['appointments'] = serializer_class.data

    wait_time = Appointment.objects.filter(
        scheduled_time__gte=today,
        scheduled_time__lte=tomorrow,
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
        # today = datetime.strptime("2019-11-24", "%Y-%m-%d")
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
            res['check_form'] = form
            res['message'] = 'No Patient found'
            return render(request, 'checkin.html', res)
        except Patient.MultipleObjectsReturned:
            res = {}
            res['check_form'] = form
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

    return render(request, "checkin.html", {'check_form': form})


@login_required(login_url='/login')
def comfirmcheckin(request):
    
    if request.method == 'POST':

        appointment_id = request.POST.get('appointment', None)
        # appointment_id = request.GET.get('appointment', None)
        # print appointment_id

        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        endpoint = AppointmentEndpoint(access_token)

        res = endpoint.update("123", {'status': 'Arrived'})
        if res['detail'] == 'Not found.':
            print "Test"
            message = 'Sorry, fail to check in.'
            return HttpResponse(message, status=403) 

        params = {'status': 'Arrived', 'checkin_time' : now()}
        Appointment.objects.filter(id=appointment_id).update(**params)
        
        # api_data = endpoint.fetch(id=appointment_id)

        # serializer = AppointmentSerializer(data=api_data)
        # if serializer.is_valid():
        #     serializer.save()
        #     serializer.instance.check_in() 
        message = 'Successfully check in.'
        return HttpResponse(message, status=200)
    
    # return render(request, 'checkin_success.html')

    message = 'Sorry, fail to check in.'
    return HttpResponse(message, status=403)


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

