from django.db import models

# Create your models here.
class Product(models.Model):
	name = models.CharField(max_length=64)
	price = models.IntegerField()
	picture = models.ImageField()

class User(models.Model):
	first = models.CharField(max_length=64)
	last = models.CharField(max_length=64)
	money = models.IntegerField()

class Review(models.Model):
	score = models.IntegerField()
	text = models.CharField(max_length=200)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="review")
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review")


	




