from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def homeView(req):
	if req.user.owners.all():
		return render(req, 'home-organisation.html', {})
	return render(req, 'home.html', {})

# def appView(req):
# 	return render(req, 'polymer/app.html', {})

