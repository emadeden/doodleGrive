import datetime
from django.shortcuts import render , redirect 
from django.http import HttpResponse , HttpResponseRedirect
from .forms import RegisterForm  
from django.conf import settings
from myApp.views import log
from .models import G

LOG_LEVEL = settings.LOG_LEVEL


publicGroup = G.objects.get(name = 'public') 
def register(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			publicGroup.users.add(user)
			#log action
			log_record = {'user': user.username  , 'action' : 'register', 'time_stamp': str(datetime.datetime.now())}
			log(log_record, 'actions-log.json',2)
			return HttpResponseRedirect('/login')	
	else:
		form = RegisterForm()

	return render(request, "register.html", {"form":form})
	


def home(request):
	return HttpResponseRedirect('/')
	