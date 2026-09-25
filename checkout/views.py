from django.shortcuts import render, redirect
from cart.models import Cart
from customers.forms import AddressForm
from customers.models import Address

def checkout_page(request):

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    saved_address = Address.objects.filter(
    session_key=session_key
).order_by("-created_at").first()

    cart = Cart.objects.get(
        session_key=session_key
    )

    cart_items = cart.items.select_related("product")

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    if request.method == "POST":

        address_form = AddressForm(request.POST)

        if address_form.is_valid():

            address = address_form.save(
                commit=False
            )

            address.session_key = session_key

            address.save()

            return redirect("checkout")

    else:

        address_form = AddressForm()

    return render(
        request,
        "checkout/checkout.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "total": total,
            "address_form": address_form,
            "saved_address": saved_address,
        }
    )