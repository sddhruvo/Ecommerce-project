from django.db import models

from products.models import Product
from profiles.models import Profile


class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)

    date_orderd = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'order-{self.id}'

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_item(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total