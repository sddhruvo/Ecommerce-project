from django.urls import path
from .views import ProductList, ProfileDetailReview

app_name = 'products'
urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('details/<int:id>/', ProfileDetailReview.as_view(), name='product_detail'),

]