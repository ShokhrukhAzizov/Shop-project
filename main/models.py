from django.db import models
from django.contrib.auth.models import AbstractUser
from slugify import slugify


class UserModel(AbstractUser):
    img = models.ImageField(upload_to='images/', null=True)

    class Meta(AbstractUser.Meta):
        swappable ='AUTH_USER_MODEL'
        verbose_name='User'
        verbose_name_plural='Users'


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photo')
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     slug = slugify(f"{self.name}")
    #     self.slug=slug
    #     super(Category, self).save(*args, **kwargs)        

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images/%y/%m/%d/')
    price = models.DecimalField(max_digits=9,decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    quantity = models.SmallIntegerField()
    is_sold = models.BooleanField(default=False)
    review = models.SmallIntegerField(blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # slug = slugify(f"{self.title}121212121")
        # self.slug=slug
        super(Product, self).save(*args, **kwargs)

class ProductCard(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    card = models.ForeignKey('Card', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=True)
    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         card  = self.card
    #         card.price +=self.product.price
    #         card.save()
    #         ProductCard.save(self, *args, **kwargs)


class ProductReview(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    rating = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.rating

    def save(self, *args, **kwargs):
        if self.pk is None:
            raitings = ProductReview.objects.filter(product=self.product)
            raiting_quantity = raitings.count()+1
            raitings_rw = 0
            for i in raitings:
                raitings_rw += i.rating
            raitings_rw += self.rating
            current = raitings_rw/raiting_quantity
            product = self.product
            product.review = current
            product.save()
            Product.save(self, *args, **kwargs)


class Card(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9,decimal_places=2, null=True, blank=True)
    # created
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    card = models.ForeignKey(Card,on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Reserved(models.Model):
    card = models.ForeignKey(Card,on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    is_active= models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Wishlist(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Company(models.Model):
    about_us = models.CharField(max_length=255)
    phone_number = models.PositiveIntegerField()
    address = models.TextField()
    email = models.EmailField()
    social_media = models.TextField()

    def __str__(self):
        return self.about_us


class Message(models.Model):
    name = models.CharField(max_length=150)
    body = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-date']

class Likee(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class Watched(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)