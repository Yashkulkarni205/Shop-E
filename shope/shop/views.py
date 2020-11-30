from .models import Product, ProductImage, UserDetail, Order
from .forms import ProductForm, ProductImageForm, UserDetailForm, ContactForm
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from . import Checksum
import uuid

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';

# Create your views here.
def admin_only(func):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'shop/not_authorized.html')
    return wrap

class AdminOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, 'shop/not_authorized.html')

def home(request):
    return render(request, 'shop/base.html')

def sup(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session['cart']
    return HttpResponse(str(len(cart)))

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')

            send_mail('Confirmation Email: Our Website', 'We Have got your Mail, We will contact you soon.' , from_email=email, recipient_list=[email])

            messages.success(request,f"Thank You {name} Your form is submitted we'll contact you soon.")
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'shop/contact.html', { 'form': form })

class ProductListView(ListView):
    model = ProductImage
    template_name = 'shop/products.html'
    context_object_name = 'products'

@admin_only
def product_create(request):

    if request.method == 'POST':
        p_form = ProductForm(request.POST)
        img_form = ProductImageForm(request.POST, request.FILES)
        if p_form.is_valid() and img_form.is_valid():
            p_form.save()
            img_form.instance.product = p_form.instance
            img_form.save()
            name = p_form.cleaned_data.get('name')
            messages.success(request,f"Product - {name} Successfully Added")
            return redirect('home')

    else:
        p_form = ProductForm()
        img_form = ProductImageForm()

    return render(request, 'shop/product_create.html', { 'p_form': p_form, 'img_form': img_form })

class ProductDetailView(DetailView):
    model = ProductImage
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

@admin_only
def product_update(request, pk):
    product = Product.objects.get(id=pk)
    productimg = ProductImage.objects.get(product=product)
    p_form = ProductForm(instance=product)
    img_form = ProductImageForm(instance=productimg)

    if request.method == 'POST':
        p_form = ProductForm(request.POST,instance=product)
        img_form = ProductImageForm(request.POST,request.FILES,instance=productimg)
        if p_form.is_valid() and img_form.is_valid():
            p_form.save()
            img_form.instance.product = p_form.instance
            img_form.save()
            name = p_form.cleaned_data.get('name')
            messages.success(request,f"Product - {name} Successfully Updated")
            return redirect('home')

    return render(request, 'shop/product_update.html', { 'p_form': p_form, 'img_form': img_form })

class ProductDeleteView(AdminOnlyMixin, DeleteView):
    model = Product
    template_name = 'shop/product_delete.html'
    context_object_name = 'product'
    success_url = '/'


class ProductByCategory(ListView):
    model = ProductImage
    template_name = 'shop/product_category.html'
    context_object_name = 'products'
    
    def get_queryset(self,**kwargs):
        category=self.kwargs['category']
        list = []
        for product in Product.objects.filter(category=category):
            list.append(ProductImage.objects.get(product=product))
        
        return list
    
def add_to_cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session['cart']
    cart[request.POST.get('name')] = 1
    request.session['cart'] = cart
        
    return HttpResponse('')
                
def cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session['cart']

    products =[]

    for name,quantity in cart.items():
        product = ProductImage.objects.filter(product= Product.objects.filter(name=name).first()).first()
        quantity = quantity
        products.append([product,quantity])    

    if request.method == 'POST':
        name=request.POST.get('name')
        quan = request.POST.get('quan')
        cart[name] += int(quan)

        if cart[name]<=0:
            cart.pop(name)

        request.session['cart'] = cart

        products =[]

        for name,quantity in cart.items():
            product = ProductImage.objects.filter(product= Product.objects.filter(name=name).first()).first()
            quantity = quantity
            products.append([product,quantity])    
    
        return render(request,'shop/cart_table.html',{ 'products': products })

    return render(request,'shop/cart.html',{ 'products': products })

@login_required
def checkout(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
        
    cart = request.session['cart']

    user_detail = UserDetail.objects.filter(user=request.user)
    if user_detail.exists():
            user_detail = UserDetail.objects.get(user=request.user)
            form = UserDetailForm(instance=user_detail)
    else:
            form = UserDetailForm()

    if request.method == 'POST':
        user_detail = UserDetail.objects.filter(user=request.user)
        
        if user_detail.exists():
            user_detail = UserDetail.objects.get(user=request.user)
            form = UserDetailForm(request.POST,instance=user_detail)
        else:
            form = UserDetailForm(request.POST)
        
        if form.is_valid():
            form.instance.user = request.user
            form.save()

            amount = 0
            for name,quantity in cart.items():
                product=Product.objects.get(name=name)
                price = product.price

                for i in price:
                    if i.isdigit() == False:
                        price = price.replace(i,'')
                
                amount += (int(price) * quantity)
            
            id = str(uuid.uuid4())
            
            param_dict={

            'MID': 'WorldP64425807474247',
            'ORDER_ID': id,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': str(request.user.email),
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'https://shopecommerce.herokuapp.com/callback/',
            }

            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
            
            return  render(request, 'shop/payment_gateway.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html', { 'form': form })

@csrf_exempt
def callback(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            return redirect('place-order')

        else:
            messages.error(request,f'{response_dict["RESPMSG"]} - Could Not Complete Your request. Try Again Later')
            
    return redirect('home')

def placeorder(request):
    user_detail = UserDetail.objects.get(user=request.user)

    if 'cart' not in request.session:
        request.session['cart'] = {}
        
    cart = request.session['cart']

    for name,quantity in cart.items():
        image = ProductImage.objects.get(product=Product.objects.get(name=name))
        order = Order.objects.create(image= image, quantity = quantity, price = image.product.price, phone = user_detail.phone, adrress = user_detail.adrress, city = user_detail.city, state = user_detail.state, country = user_detail.country, pincode = user_detail.pincode)
        order.user.add(request.user)
            
    cart.clear()
    request.session['cart'] = cart

    messages.success(request,"Order Successfully Placed")

    return redirect('home')

def orders(request):
    if request.method == 'POST':
        image = ProductImage.objects.get(product=Product.objects.get(name=request.POST.get('name')))
        Order.objects.filter(user=request.user, image=image).delete()

        return render(request,'shop/order_table.html',{
        'orders':  Order.objects.filter(user=request.user)
    })

    return render(request,'shop/orders.html',{
        'orders':  Order.objects.filter(user=request.user)
    })


