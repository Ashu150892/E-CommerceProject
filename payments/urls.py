from django.urls import path

from .views import payment_page, dummy_payment


urlpatterns = [

    path(
        "<str:order_number>/",
        payment_page,
        name="payment_page"
    ),

    path(
        "<str:order_number>/dummy/",
        dummy_payment,
        name="dummy_payment"
    ),

]