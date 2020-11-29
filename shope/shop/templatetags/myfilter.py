from django import template

register = template.Library()

@register.filter(name='commasremove')
def commasremove(price):
    for i in price:
        if i.isdigit() == False:
            price = price.replace(i,'')

    return int(price)

@register.filter(name='commasadd')
def commasradd(price):
    price = str(price)
    if len(price)>3:
        for i in range(-3,-len(price)-1,-3):
            price = price[:i] + ',' + price[i:]
    return price

@register.filter(name='multiply')
def multiply(price, quantity):
    price = commasremove(price)
    return commasradd(price*quantity)

@register.filter(name='total')
def total(products):
    total = 0 
    for product,quantity in products:
        total += (commasremove(product.product.price) * quantity)

    return commasradd(total)
