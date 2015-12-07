from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth
from vragenlijsten.views import manageView
from ajax_select import urls as ajax_select_urls


urlpatterns = [
    url(r'^api/', include('vragenlijsten.urls'), name='api'),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('mediaprofielen_front.urls')),
    url(r'^manage/', manageView, name='manage'),
]

