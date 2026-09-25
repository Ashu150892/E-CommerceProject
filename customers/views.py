from django.shortcuts import render
from cart.models import Cart
from customers.forms import AddressForm


def checkout_page(request):

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    cart = Cart.objects.get(
        session_key=session_key
    )

    cart_items = cart.items.select_related("product")

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    address_form = AddressForm()

    return render(
        request,
        "checkout/checkout.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "total": total,
            "address_form": address_form,
        }
    )