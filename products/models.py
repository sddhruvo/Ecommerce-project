import uuid
from django.db import models
from django.urls import reverse
from django.db.models import Avg, Count, Sum
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from profiles.models import Profile #local import


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']
    """
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
    """
    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])



class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE) #many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(upload_to='product_images/', null=True, default='default-book.jpg')
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    amount=models.IntegerField(default=0)
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10,choices=STATUS)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title   

    @property
    def get_total_review(self):
        total_review = self.review_set.count()
        return total_review

    @property
    def get_total_rating(self):
        total_rating = self.review_set.annotate(total_rating=Sum('rating')).aggregate(Avg('total_rating'))
        return total_rating['total_rating__avg']
    

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'id': self.id})


class Review(models.Model):
    Rating_CHOICES = (
    (1, 'Poor(1)'),
    (2, 'Average(2)'),
    (3, 'Good(3)'),
    (4, 'Very Good(4)'),
    (5, 'Excellent(5)')
    )

    title = models.CharField(max_length=50)
    description = models.TextField()
    post = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=Rating_CHOICES, default=3)

    def __str__(self):
        return self.title

    
    

