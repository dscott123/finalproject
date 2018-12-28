from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from orders.models import Account, Inventory
from django.http import HttpResponse, Http404
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUp(generic.CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy("login")
	template_name = "registration/signup.html"

@login_required
def create(request):
	Account.objects.create(owner=request.user)
	context = {
		"user": request.user
	}
	return render(request, "accounts/account.html", context)

@login_required
def account(request):
	user = request.user
	inventory = Inventory.objects.filter(account=user.account)
	context = {
		"user": user,
		"inventory": inventory
	}
	return render(request, "accounts/account.html", context)

@login_required
def money(request):
	try:
		account = Account.objects.get(owner=request.user)
	except:
		raise Http404("No account exists")
	current = account.money
	account.money = current + 100
	account.save()
	user = request.user
	inventory = Inventory.objects.filter(account=user.account)
	context = {
		"user": user,
		"inventory": inventory
	}
	return render(request, "accounts/account.html", context)

@login_required
def name(request):
	context = {
		"user": request.user
	}
	return render(request, "accounts/info.html", context)

@login_required
def change_name(request):
	user = request.user
	user.first_name = request.POST.get('firstname')
	user.last_name = request.POST.get('lastname')
	user.email = request.POST.get('email')
	user.save()
	inventory = Inventory.objects.filter(account=user.account)
	context = {
		"user": user,
		"inventory": inventory
	}
	return render(request, "accounts/account.html", context)