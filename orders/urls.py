from django.urls import path
from .views import cart, update_item, checkout, buy_product


app_name = 'orders'
urlpatterns = [
    path('', cart, name='cart'),
    path('update-item/', update_item, name='update_item'),
    path('checkout/', checkout, name='checkout'),
    path('buy-product/', buy_product, name='buy_product'),


]