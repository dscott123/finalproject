from django.http import HttpResponse, Http404
from django.shortcuts import render

from .models import Product
# Create your views here.
def index(request):
	context = {
		"products": Product.objects.all()
	}
	return render(request, "orders/index.html", context)

def product(request, product_id):
	try:
		product = Product.objects.get(pk=product_id)
	except Product.DoesNotExist:
		raise Http404("Product does not exist")
	context = {
		"product": product,
		"reviews": product.review.all()
	}
	return render(request, "orders/product.html", context)