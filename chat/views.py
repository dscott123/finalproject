from django.http import HttpResponse, Http404
from django.shortcuts import render
from orders.models import Room

# Create your views here.
def chat(request):
	rooms = Room.objects.all()
	context = {
		"rooms": rooms
	}

	return render(request, "chat/chat.html", context)