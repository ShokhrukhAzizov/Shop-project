from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photo')

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images/%y/%m/%d/')
    price = models.DecimalField(max_digits=9,decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    quantity = models.SmallIntegerField()
    is_sold = models.BooleanField(default=False)
    review = models.SmallIntegerField()

class Card(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    is_active = models.BooleanField(default=True)

class Order(models.Model):
    card = models.ForeignKey(Card,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

class Reserved(models.Model):
    card = models.ForeignKey(Card,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_active= models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)



class Company(models.Model):
    about_us = models.CharField(max_length=255)
    phone_number = models.PositiveIntegerField()
    address = models.TextField()
    email = models.EmailField()
    social_media = models.TextField()

class Message(models.Model):
    name = models.CharField(max_length=150)
    body = models.TextField()
    email = models.EmailField()