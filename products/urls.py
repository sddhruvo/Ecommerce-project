from django.urls import path
from .views import ProductList, ProductDetail

app_name = 'products'
urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('details/<int:id>/', ProductDetail.as_view(), name='product_detail'),

]