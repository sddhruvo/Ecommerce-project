import uuid
from django.db import models
from profiles.models import Profile



class Category(models.Model):
    title = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.title



class Product(models.Model):
    title = models.CharField(max_length=200, blank=False)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    dealer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='product')
    category = models.ManyToManyField(Category, related_name='product_category')
    description = models.CharField(max_length=5000, blank=False)
    price = models.DecimalField(verbose_name='Product Price',max_digits=5, decimal_places=2)
    image = models.ImageField(verbose_name='Product Cover', default='default.jpg', upload_to='product/')
    stock = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.title}-p:{self.price}'
    

