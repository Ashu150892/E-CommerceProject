from django.urls import path

from .views import (
    customer_login,
    verify_otp,
    customer_profile,
    edit_profile,
)


urlpatterns = [

    path(
        "login/",
        customer_login,
        name="customer_login"
    ),

    path(
        "verify-otp/",
        verify_otp,
        name="verify_otp"
    ),

    path(
        "profile/",
        customer_profile,
        name="customer_profile"
    ),

    path(
        "profile/edit/",
        edit_profile,
        name="edit_profile"
    ),

]