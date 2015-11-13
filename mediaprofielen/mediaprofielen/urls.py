from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth
from vragenlijsten.views import manageView


urlpatterns = [
    url(r'^api/', include('vragenlijsten.urls'), name='api'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('mediaprofielen_front.urls')),
    url(r'^manage/', manageView, name='manage')
]

