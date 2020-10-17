from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from .models import Profile

User = get_user_model()


class ProfileDetailView(LoginRequiredMixin, DetailView):

    model = Profile
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        context ['products'] = self.object.bought_product.all()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = Profile
    fields = ["first_name", 'last_name', 'gender', 'address', 
        'phone_number',
    ]

    def get_success_url(self):
        return reverse("profiles:profile_detail", kwargs={"slug": self.request.user.username})

    def get_object(self):
        return Profile.objects.get(id=self.request.user.id)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


class ProfileRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("profiles:profile_detail", kwargs={"slug": self.request.user.username})
