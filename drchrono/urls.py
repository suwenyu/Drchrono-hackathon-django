from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

import views


urlpatterns = [
	url(r'^init/$', views.synchron_db, name='init'),
	url(r'^index/$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'logout/$', views.logout, name='logout'),

    url(r'^checkin/$', views.checkin, name='checkin'),
    url(r'^comfirmcheckin/$', views.comfirmcheckin, name='comfirmcheckin'),
    url(r'^appointment/start/(?P<appointment>\d+)', views.startAppointments, name='startappointment'),
    url(r'^appointment/finish/(?P<appointment>\d+)', views.finishAppointments, name='finishappointment'),
    url(r'^appointment/cancel/(?P<appointment>\d+)', views.cancelAppointments, name='cancelappointment'),

    url(r'^patient/update/(?P<patient>\d+)$', views.update_patient_info, name="update_patient_info"),

	url(r'test1/$', views.test1, name='test'),    

    # url(r'^checkin/(?P<appointment_id>\d+)/$', views.comfirmCheckIn, name='confirm_appointment'),)
    # url(r'^welcome/$', views.DoctorWelcome.as_view(), name='setup'),
    # url(r'^test/$', views.TestAppointment.as_view(), name='test'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]