from django.conf.urls import patterns, url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.decorators import login_required
from vragenlijsten import views
from vragenlijsten.views import currentUserView, maxPointsView
from views import *

import django.contrib.auth

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'enquetes', EnqueteViewSet)
router.register(r'blocks', BlockViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'organisations', OrganisationViewSet)
router.register(r'accounts', AccountViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^changepassword/$', changePasswordView.as_view(), name='currentuser'),
	url(r'^currentuser/$', currentUserView.as_view(), name='currentuser'),
	url(r'^currentorganisation/$', currentOrganisationView.as_view(), name='currentorganisation'),
	url(r'^maxpoints/$', maxPointsView.as_view(), name='maxpoints'),
	url(r'^csv/([0-9]+)$', csv_view, name='csv')
]