from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:product_id>", views.product, name="product"),
    path("addcart/", views.addcart, name="addcart"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("remove/", views.remove, name="remove")
]
