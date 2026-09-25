from django.urls import path
from .views import checkout_page


urlpatterns = [
    path("", checkout_page, name="checkout"),
]