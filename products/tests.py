import uuid
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from .models import Product, Category
from profiles.models import CustomUser


class BlogTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = CustomUser.objects.create_user(username='testuser1', password='testpassword13546')
        testuser1.save()

        # creates category
        test_category = Category.objects.create(title='Electronics')

        #creates product
        test_product = Product.objects.create(dealer=testuser1.profile, title='test product',
        description = 'test description', stock = 2, price = 500)
        test_product.save()

    def test_product(self):
        product = Product.objects.get(title = 'test product')
        dealer = f'{product.dealer}'
        title = f'{product.title}'
        description = f'{product.description}'
        price = f'{product.price}'
        stock = f'{product.stock}'
        self.assertEqual(dealer, 'testuser1')
        self.assertEqual(title, 'test product')
        self.assertEqual(description, 'test description')
        self.assertEqual(int(stock), 2)
        self.assertEqual(price, '500.00')