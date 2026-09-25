import uuid

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import Cart
from customers.models import Address
from payments.models import Payment

from .models import Order, OrderItem


def place_order(request):

    if request.method != "POST":
        return redirect("checkout")

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    cart = get_object_or_404(
        Cart,
        session_key=session_key
    )

    cart_items = cart.items.select_related("product")

    if not cart_items.exists():
        return redirect("cart_page")

    address = Address.objects.filter(
        session_key=session_key
    ).order_by("-created_at").first()

    if not address:
        return redirect("checkout")

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    order_number = f"ORD-{uuid.uuid4().hex[:10].upper()}"

    with transaction.atomic():

        order = Order.objects.create(
            order_number=order_number,
            session_key=session_key,
            address=address,
            total_amount=total,
            status="NEW",
        )

        Payment.objects.create(
            order=order,
            payment_method="COD",
            payment_status="PENDING",
            amount=total,
        )

        for item in cart_items:

            subtotal = item.product.price * item.quantity

            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
                subtotal=subtotal,
            )

        cart_items.delete()

    return redirect(
        "payment_page",
        order_number=order.order_number
    )


def order_success(request, order_number):

    order = get_object_or_404(
        Order,
        order_number=order_number,
        session_key=request.session.session_key
    )

    status_steps = [
        ("NEW", "New"),
        ("CONFIRMED", "Confirmed"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
    ]

    return render(
        request,
        "orders/order_success.html",
        {
            "order": order,
            "status_steps": status_steps,
        }
    )

def order_history(request):

    if not request.session.session_key:
        request.session.create()

    orders = Order.objects.filter(
        session_key=request.session.session_key
    ).prefetch_related(
        "items"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "orders/order_history.html",
        {
            "orders": orders,
        }
    )