import uuid
from django.db import models

class Item(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    productId = models.IntegerField(default=0)

class Sales(models.Model):
    totalProfit = models.DecimalField(decimal_places=2, max_digits=10)
    stockSold = models.IntegerField(default=0)

class Sale(models.Model):
    products = models.ManyToManyField(Item)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

class ProductIdCount(models.Model):
    countType = models.CharField(max_length=200)
    count = models.IntegerField(default=100)