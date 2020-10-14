from django.urls import path
from .views import cart, update_item


app_name = 'orders'
urlpatterns = [
    path('', cart, name='cart'),
    path('update-item/', update_item, name='update_item')
]