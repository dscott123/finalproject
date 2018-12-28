from django.db import models
from django.conf import settings


# Create your models here.

class Product(models.Model):
	name = models.CharField(max_length=64)
	price = models.IntegerField()
	description = models.TextField(default="  ")
	picture = models.ImageField()
	
class Account(models.Model):
	money = models.IntegerField(default=100)
	cart = models.ManyToManyField(Product, through='InCart')
	inventory = models.ManyToManyField(Product, through='Inventory', related_name="owner")
	owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="account")

class Review(models.Model):
	score = models.IntegerField()
	text = models.TextField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="review")
	author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="review")

class InCart(models.Model):
	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	amount = models.IntegerField(default=0)

class Inventory(models.Model):
	account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="storage")
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	amount = models.IntegerField(default=0)

class Room(models.Model):
	name = models.TextField()
	staff_only = models.BooleanField(default=False)
	def __str__(self):
		return self.name
	@property
	def group_name(self):
		return "room-%s" % self.id

	


