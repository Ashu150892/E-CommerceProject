from django.shortcuts import get_object_or_404, redirect, render

from orders.models import Order
from .models import Payment


def payment_page(request, order_number):

    order = get_object_or_404(
        Order,
        order_number=order_number,
        session_key=request.session.session_key
    )

    if request.method == "POST":

        payment_method = request.POST.get("payment_method")

        if payment_method not in ["COD", "ONLINE"]:
            return render(
                request,
                "payments/payment.html",
                {
                    "order": order,
                    "error": "Please select a valid payment method.",
                }
            )

        Payment.objects.update_or_create(
            order=order,
            defaults={
                "payment_method": payment_method,
                "payment_status": "PENDING",
                "amount": order.total_amount,
            }
        )

        if payment_method == "COD":
            return redirect(
                "order_success",
                order_number=order.order_number
            )

        return redirect(
            "dummy_payment",
            order_number=order.order_number
        )

    return render(
        request,
        "payments/payment.html",
        {
            "order": order,
        }
    )


def dummy_payment(request, order_number):

    order = get_object_or_404(
        Order,
        order_number=order_number,
        session_key=request.session.session_key
    )

    payment = get_object_or_404(
        Payment,
        order=order
    )

    if request.method == "POST":

        card_number = request.POST.get("card_number")

        if card_number == "4111111111111111":

            payment.payment_status = "SUCCESS"
            payment.transaction_id = (
                f"DUMMY-{order.order_number}"
            )
            payment.save()

            return redirect(
                "order_success",
                order_number=order.order_number
            )

        elif card_number == "4000000000000002":

            payment.payment_status = "FAILED"
            payment.transaction_id = (
                f"DUMMY-FAILED-{order.order_number}"
            )
            payment.save()

            return render(
                request,
                "payments/dummy_payment.html",
                {
                    "order": order,
                    "payment_failed": True,
                }
            )

        else:

            return render(
                request,
                "payments/dummy_payment.html",
                {
                    "order": order,
                    "invalid_card": True,
                }
            )

    return render(
        request,
        "payments/dummy_payment.html",
        {
            "order": order,
        }
    )