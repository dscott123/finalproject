from django.urls import path

from . import views


urlpatterns= [
	path('signup/', views.SignUp.as_view(), name="signup"),
	path('create/', views.create, name="create"),
	path('account/', views.account, name="account"),
	path('money/', views.money, name="money"),
	path('name/', views.name, name="name"),
	path('change_name/', views.change_name, name="change_name")
]