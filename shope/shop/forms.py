from django import forms
from .models import Product, ProductImage, UserDetail, Contact

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','price','category']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['phone','adrress' ,'city','state','country','pincode']

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name','email','message']