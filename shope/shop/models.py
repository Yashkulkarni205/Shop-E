from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=95)
    email = models.EmailField(max_length=35)
    message = models.TextField()

    def __str__(self):
        return self.name 

class Product(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    price = models.CharField(max_length=10)
    category = models.TextChoices('category','clothing electronics food')
    category = models.CharField(max_length = 20, blank=True, choices = category.choices)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'image')

    def __str__(self):
        return str(self.product) + ' Image'

    def save(self):
        super().save()  # saving image first

        img = Image.open(self.image.path) # Open image using self
        
        new_img = (240, 360)
        img.thumbnail(new_img)
        img.save(self.image.path)

class UserDetail(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = PhoneNumberField(default='+91')
    adrress = models.CharField(max_length=95)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    country = models.CharField(max_length=35)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return str(self.user) + '-Details'

class Order(models.Model):
    user = models.ManyToManyField(User)
    image = models.ForeignKey(ProductImage,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.CharField(max_length=10)
    phone = PhoneNumberField(default='+91')
    adrress = models.CharField(max_length=95)
    city = models.CharField(max_length=35)
    pincode = models.CharField(max_length=6)
    state = models.CharField(max_length=35)
    country = models.CharField(max_length=35)

    def __str__(self):
        return str(self.product) + '-' + str(self.user.all()[0])

