from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def landing(request):
	if request.user.is_superuser:
		return HttpResponseRedirect('/adminf/home/')
	return render(request,'BasicFunc/landing.html')

def user_login(request):
	if request.method == 'POST':
		uname = request.POST['username']
		passw = request.POST['password']
		user = authenticate(username=uname, password=passw)
		if user:
			login(request, user)
			data = User.objects.get(id=user.id)
			if data.is_superuser:
				return HttpResponseRedirect('/adminf/home')
			elif data.is_staff:
				return HttpResponse('<h1>Staff</h1>')
			else:
				return HttpResponse('Student Home calling')
		else:
			return render(request,'BasicFunc/login.html',{'msg':'Wrong credentials! try again.'})
	else:
		return render(request,'BasicFunc/login.html')