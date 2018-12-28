from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product, Account, InCart, Inventory
# Create your views here.


def index(request):
	if request.user.is_authenticated:
		user = request.user
	else:
		user = None
	context = {
		"products": Product.objects.all(),
		"user": user
	}	
	return render(request, "orders/index.html", context)

def product(request, product_id):
	try:
		product = Product.objects.get(pk=product_id)
	except Product.DoesNotExist:
		raise Http404("Product does not exist")
	if request.user.is_authenticated:
		user = request.user
	else:
		user = None
	context = {
		"product": product,
		"reviews": product.review.all(),
		"user": user
	}
	return render(request, "orders/product.html", context)

@login_required
def cart(request):
	user = request.user
	account = Account.objects.get(owner=user)
	cart = InCart.objects.filter(account=account)
	money = account.money
	price = 0
	success = True
	for products in cart:
		price += (products.product.price * products.amount)
	final_money = money - price
	context = {
		"user": user,
		"cart": cart,
		"price": price,
		"final_money": final_money,
		"success": success
	}
	return render(request, "orders/cart.html", context)

@login_required
def addcart(request):
	product_id = request.POST.get('product')
	product = Product.objects.get(pk=product_id)
	user = request.user
	amount = request.POST.get('amount')
	try:
		cart = InCart.objects.get(account=user.account, product=product)
		cart.amount+=amount
		cart.save()
	except:
		InCart.objects.create(account=user.account, product=product, amount=amount)
	context = {
		"product": product,
		"reviews": product.review.all(),
		"user": user
	}
	return render(request, "orders/product.html", context)

@login_required
def checkout(request):
	user = request.user
	price = request.POST.get('price')
	money = user.account.money
	if int(money) - int(price) >= 0:
		user.account.money = int(money)-int(price)
		user.account.save()
		cart = InCart.objects.filter(account=user.account)
		for product in cart:
			item = product.product
			try:
				inventory = Inventory.objects.get(account=user.account, product=product.product)
				inventory.amount+=product.amount
				inventory.save()
			except:
				Inventory.objects.create(account=user.account, product=product.product, amount=product.amount)
		cart.delete()
		success = True
	else:
		success = False
	cart = InCart.objects.filter(account=user.account)
	price = 0
	for products in cart:
		price += (products.product.price * products.amount)
	final_money = money - price
	context = {
		"user": user,
		"cart": cart,
		"price": price,
		"final_money": final_money,
		"success": success
	}
	return render(request, "orders/cart.html", context)

@login_required
def remove(request):
	user = request.user
	product_id = request.POST.get('product')	
	amount = request.POST.get('amount')
	try:
		if request.POST.get('remove_all') == 'yes':
			cart = InCart.objects.filter(account=user.account)
			cart.delete()
		else:
			cart = InCart.objects.get(account=user.account, product=product_id)
			if int(cart.amount) - int(amount) <= 0:
				cart.delete()
			else:
				cart.amount = int(cart.amount) - int(amount)
				cart.save()
	except:
		raise Http404('An Error Occured')
	account = Account.objects.get(owner=user)
	full_cart = InCart.objects.filter(account=account)
	money = account.money
	price = 0
	for products in full_cart:
		price += (products.product.price * products.amount)
	final_money = money - price
	context = {
		"user": user,
		"cart": full_cart,
		"price": price,
		"final_money": final_money
	}
	return render(request, "orders/cart.html", context)