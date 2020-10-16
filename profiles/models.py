import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver



class CustomUser(AbstractUser):
    """Default user for stalker_project."""

    #: First and last name do not cover name patterns around the globe
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
 
User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    GENDER = [
        ('NONE', 'none'),
        ('MALE', 'male'),
        ('FEMALE', 'female')
    ]
    
    first_name = models.CharField(max_length=128, null=True, blank=False)
    last_name = models.CharField(max_length=128, null=True)
    id = models.UUIDField(primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=6, choices=GENDER, default='NONE')
    address = models.CharField(max_length=500, blank=False)
    phone_number = models.CharField(max_length=20, blank=True)
    slug = models.SlugField(unique=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True, blank=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.id = self.user.id
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def get_full_name(self):
        if self.first_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.user.username

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail."""

        return reverse("profiles:detail", kwargs={"slug": self.username.lower()})


class Wallet(models.Model):
    """ virtual wallet model for each user """
    balance = models.IntegerField(default=0)
    user = models.OneToOneField(Profile, on_delete = models.CASCADE, related_name='wallet')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.slug}-B:{self.balance}"

class BoughtProduct(models.Model):
    from products.models import Product # Product imported here to avoid cyclic import error

    user = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='bought_product', null=True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    active_for_resell = models.BooleanField(default=False)

    def __str__(self):
        return f"Owner:{self.user.user.username}-pro:{self.product.title}"


# signal to create profile for user created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Wallet.objects.create(user=instance.profile, balance=200)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.profile.wallet.save()