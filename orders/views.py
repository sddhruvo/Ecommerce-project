import json
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import *
from products.models import Product
from profiles.models import BoughtProduct, Wallet
from orders.models import OrderItem


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer,)
        items = order.orderitem_set.all()

    else:
        items = []
        order = {"get_cart_total": 0, 'get_cart_item': 0}
    context = {'items':items, 'order': order}
    return render(request, 'orders/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer,)
        items = order.orderitem_set.all()

    else:
        items = []
        order = {"get_cart_total": 0, 'get_cart_item': 0}
    context = {'items':items, 'order': order}
    return render(request, 'orders/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user.profile
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1

    order_item.save()

    if order_item.quantity <= 0 or action == 'full-remove':
        order_item.delete()

    return JsonResponse('item added', safe=False)

def buy_product(request):
    """
    need to add message of quatity error
    """
    order = Order.objects.get(customer=request.user.profile)
    items = order.orderitem_set.all()
    for item in items:
        product = Product.objects.get(id=item.product.id)
        order_item = OrderItem.objects.get(id=item.id)
        wallet = Wallet.objects.get(user=request.user.profile)
        if product.stock >= item.quantity and wallet.balance >= (item.quantity*item.product.price):
            BoughtProduct.objects.create(
                user=request.user.profile, product = item.product,
                quantity = item.quantity, price=item.product.price
            )
            
            product.stock = product.stock - item.quantity
            product.save()
            order_item.delete()
            wallet.balance = wallet.balance - (item.quantity*item.product.price)
            wallet.save()
        else:
            return redirect('orders:cart')

    
    return redirect('profiles:profile_detail', slug=request.user.username)
        
    
