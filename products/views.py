from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Product, Review
from .forms import ReviewModelForm
from profiles.models import Profile


class ProductList(ListView):
    model = Product
    ordering = '-created_at'

class ProductDetail(DetailView):
    model = Product
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        context ['reviews'] = self.object.review_set.all()
        context['form'] = ReviewModelForm()
        return context

class ProductReview(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'products/product_detail.html'
    form_class = ReviewModelForm
    model = Product

    def post(self, request, *args, **kwargs):
        """ 
        validate review form in product detail page
        """

        review_form = ReviewModelForm()
        profile=Profile.objects.get(user=request.user)
        if 'submit_r_form' in request.POST:
            review_form = ReviewModelForm(request.POST or None)
            if review_form.is_valid():
                instance = review_form.save(commit=False)
                instance.author = profile
                product_id = request.POST.get('product_id')
                instance.post = Product.objects.get(id=product_id)
                instance.save()
                review_form = ReviewModelForm()
                return HttpResponseRedirect(self.request.path_info)


    def get_success_url(self):
        return reverse("products:detail", kwargs={"id": self.id})         

class ProfileDetailReview(View):
    """
    If request contain get then return ProductDetail view
    if request contains post method then return return ProductReview method
    """
    def get(self, request, *args, **kwargs):
        view = ProductDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProductReview.as_view()
        return view(request, *args, **kwargs)
