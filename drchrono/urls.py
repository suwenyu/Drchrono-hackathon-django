from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

import views

from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'snippets', views.SnippetViewSet)
router.register(r'appointments', views.AppointmentViewSet)


urlpatterns = [
	url(r'^init/$', views.synchron_db, name='init'),
	# url(r'^index/$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'logout/$', views.logout, name='logout'),

    url(r'^checkin/$', views.PatientCheckIn.as_view(), name='checkin'),
    
    url(r'^patientinfo/(?P<patient>\d+)/update', views.PatientUpdateInfo.as_view(), name='patientinfo_upd'),
	# url(r'^test1/$', views.test1, name='test'),    

    # url(r'^checkin/(?P<appointment_id>\d+)/$', views.comfirmCheckIn, name='confirm_appointment'),)
    # url(r'^welcome/$', views.DoctorWelcome.as_view(), name='setup'),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', views.IndexViewSet.as_view(), name='index'),
    url(r'^', include(router.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]