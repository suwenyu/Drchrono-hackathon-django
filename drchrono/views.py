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
from django.views.generic.edit import FormView

from drchrono.sync import synchron_all_data

from datetime import datetime, timedelta
from django.utils.timezone import now

from django.db import models

from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

def login(request):
    if request.user.is_authenticated():
        return redirect('index')

    return render(request, 'kiosk_setup.html')


@login_required(login_url='/login')
def logout(request):
    django_logout(request)
    return redirect('login')


@login_required(login_url='/login')
def synchron_db(request):
    synchron_all_data()
    return redirect('index')


class IndexViewSet(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = retrieveAppointmentSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request):
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']


        api = DoctorEndpoint(access_token)
        doctor = next(api.list())
        request.session['doctor'] = doctor['id']

        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today = datetime.strptime("2019-12-16", "%Y-%m-%d")
        
        tomorrow = today + timedelta(days=1)

        queryset = Appointment.objects.filter(
            scheduled_time__gte=today,
            scheduled_time__lte=tomorrow,
            doctor=doctor['id']
        ).order_by('scheduled_time')
        serializer = retrieveAppointmentSerializer(queryset, many=True)

        avg_wait_time = Appointment.objects.filter(
            scheduled_time__gte=today,
            scheduled_time__lte=tomorrow,
            doctor=doctor['id'],
            waiting_time__isnull=False
        ).aggregate(models.Avg('waiting_time'))['waiting_time__avg']
        if avg_wait_time:
            avg_wait_time = round(avg_wait_time, 2)

        return Response({'appointments': serializer.data, 'avg_wait_time' : avg_wait_time, 'current_time':now()}, template_name='index.html')


class PatientCheckIn(FormView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    template_name = 'checkin.html'
    form_class = checkin_form

    def form_valid(self, form):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # today = datetime.strptime("2019-11-27", "%Y-%m-%d")
        today = datetime.strptime("2019-12-16", "%Y-%m-%d")
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
            res['form'] = form
            res['message'] = 'No Patient found'
            return render(self.request, 'checkin.html', res)

        except Patient.MultipleObjectsReturned:
            res = {}
            res['form'] = form
            res['message'] = 'Multiple Account found'
            return render(self.request, 'checkin.html', res)
            
        # patient = Patient.objects.filter(**filters).values()
        
        appointments = Appointment.objects.filter(
            doctor=self.request.session['doctor'],
            patient=patient.id, 
            scheduled_time__gte=today, 
            scheduled_time__lte=tomorrow
        ).order_by('scheduled_time').values()

        return render(self.request, 'confirm_appointment.html', {"appointments": appointments, "patient":patient})

    def form_invalid(self, form):
        return render(self.request, "checkin.html", {'form': form})

class PatientUpdateInfo(FormView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    template_name = 'patient_info.html'
    form_class = patient_info_form

    def get_form_kwargs(self):
        kwargs = super(PatientUpdateInfo, self).get_form_kwargs()
        patient_id = self.kwargs['patient']

        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']

        api_data = PatientEndpoint(access_token).fetch(id=patient_id)
        
        kwargs.update({'initial': api_data})
        # print kwargs
        return kwargs

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context['form'] = form

        patient = Patient.objects.get(id=self.kwargs['patient'])
        context['patient'] = patient

        return render(request, 'patient_info.html', context)
    

    def form_invalid(self, form):
        patient = Patient.objects.get(id=self.kwargs['patient'])
        return render(self.request, 'patient_info.html', {'form' : form, 'patient' : patient })

    def form_valid(self, form):
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        endpoint = PatientEndpoint(access_token)

        params = {}
        for field in form.cleaned_data:
            if form.cleaned_data[field] != "" and form.cleaned_data[field] != None:
                params[field] = form.cleaned_data[field]

        endpoint.update(self.kwargs['patient'], params)

        return redirect('index')


class AppointmentViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    @action(methods=['post'], detail=False, url_name='confirm')
    def confirm(self, request):
        # print pk
        pk = request.POST.get('pk', None)

        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        endpoint = AppointmentEndpoint(access_token)

        res = endpoint.update(pk, {'status': 'Arrived'})
        api_data = endpoint.fetch(id=pk)

        try:
            model = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(model, data=api_data)

            if serializer.is_valid():
                serializer.save()

                message = 'Successfully check in.'
                return HttpResponse(message, status=200)

        except Appointment.DoesNotExist:
            pass

        message = 'Sorry, fail to check in.'
        return HttpResponse(message, status=403)

    @action(methods=['post'], detail=True, url_name='startappointment')
    def startappointment(self, request, pk=None):
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        endpoint = AppointmentEndpoint(access_token)

        endpoint.update(pk, {'status':'In Session'})
        api_data = endpoint.fetch(id=pk)

        try:
            model = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(model, data=api_data)

            if serializer.is_valid():
                serializer.save()

        except Appointment.DoesNotExist:
            pass

        return redirect('index')

    @action(methods=['post'], detail=True, url_name='endappointment')
    def endappointment(self, request, pk=None):
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        endpoint = AppointmentEndpoint(access_token)

        endpoint.update(pk, {'status':'Complete'})
        api_data = endpoint.fetch(id=pk)

        try:
            model = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(model, data=api_data)

            if serializer.is_valid():
                serializer.save()

        except Appointment.DoesNotExist:
            pass

        return redirect('index')

    @action(methods=['post'], detail=True, url_name='cancelappointment')
    def cancelappointment(self, request, pk=None):
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        endpoint = AppointmentEndpoint(access_token)

        endpoint.update(pk, {'status':'Cancelled'})
        api_data = endpoint.fetch(id=pk)

        try:
            model = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(model, data=api_data)

            if serializer.is_valid():
                serializer.save()

        except Appointment.DoesNotExist:
            pass

        return redirect('index')


@login_required(login_url='/login')
def debug(request):
    oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
    access_token = oauth_provider.extra_data['access_token']

    endpoint = PatientEndpoint(access_token)
    print next(endpoint.list())
    # queryset = Appointment.objects.all()

    # serializer_class = retrieveAppointmentSerializer(queryset, many=True)
    # content = serializer_class.data
    # print content
    return render(request, 'debug.html', {'data': next(endpoint.list())})






