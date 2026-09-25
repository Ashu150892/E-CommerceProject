from django.urls import path

from .views import (
    place_order,
    order_success,
    order_history,
)


urlpatterns = [

    path(
        "place/",
        place_order,
        name="place_order"
    ),

    path(
        "success/<str:order_number>/",
        order_success,
        name="order_success"
    ),

    path(
        "history/",
        order_history,
        name="order_history"
    ),

]