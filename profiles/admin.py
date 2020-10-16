from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from .models import Profile, Wallet, BoughtProduct
from .forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ["username", "first_name", "is_superuser"]
    search_fields = ["first_name"]


admin.site.register(Profile)
admin.site.register(Wallet)
admin.site.register(BoughtProduct)

