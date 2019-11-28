from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

import views


urlpatterns = [
    url(r'^login/$', views.SetupView.as_view(), name='login'),
    # url(r'^welcome/$', views.DoctorWelcome.as_view(), name='setup'),
    url(r'^index/$', views.index, name='index'),


    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]