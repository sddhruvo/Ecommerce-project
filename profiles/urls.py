from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView, ProfileRedirectView

app_name = 'profiles'
urlpatterns = [
    path("~redirect/", ProfileRedirectView.as_view(), name="redirect"),
    path('~update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
]