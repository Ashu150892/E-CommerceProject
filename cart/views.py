from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Cart, CartItem


def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(
        session_key=session_key
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("home")


def cart_page(request):

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(
        session_key=session_key
    )

    cart_items = cart.items.select_related("product")

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    return render(
        request,
        "cart/cart.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "total": total,
        }
    )


def increase_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect("cart_page")


def decrease_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect("cart_page")

def remove_from_cart(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )

    cart_item.delete()

    return redirect("cart_page")