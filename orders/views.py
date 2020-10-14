import json
from django.shortcuts import render
from django.http import JsonResponse

from .models import *
from products.models import Product



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
    context = {}
    return render(request, 'orders/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    print(product_id, action)

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