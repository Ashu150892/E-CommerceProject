import random
from datetime import timedelta

from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Customer, OTPVerification, Address
from .forms import CustomerProfileForm


def customer_login(request):

    if request.method == "POST":

        identifier = request.POST.get("identifier")

        if not identifier:
            return render(
                request,
                "customers/login.html",
                {
                    "error": "Please enter your email or phone number."
                }
            )

        # --------------------------------
        # Find or create customer
        # --------------------------------

        if "@" in identifier:

            customer = Customer.objects.filter(
                email=identifier
            ).first()

            if not customer:
                customer = Customer.objects.create(
                    email=identifier
                )

        else:

            customer = Customer.objects.filter(
                phone=identifier
            ).first()

            if not customer:
                customer = Customer.objects.create(
                    phone=identifier
                )

        # --------------------------------
        # Generate OTP
        # --------------------------------

        otp = str(random.randint(100000, 999999))

        expires_at = timezone.now() + timedelta(minutes=5)

        OTPVerification.objects.create(
            customer=customer,
            otp=otp,
            expires_at=expires_at
        )

        # Store customer ID in session
        request.session["login_customer_id"] = customer.id

        # --------------------------------
        # Temporary testing
        # --------------------------------

        print("================================")
        print("CUSTOMER OTP:", otp)
        print("================================")

        return redirect("verify_otp")

    return render(
        request,
        "customers/login.html"
    )


def verify_otp(request):

    customer_id = request.session.get(
        "login_customer_id"
    )

    if not customer_id:
        return redirect("customer_login")

    customer = Customer.objects.filter(
        id=customer_id
    ).first()

    if not customer:
        return redirect("customer_login")

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        otp_record = OTPVerification.objects.filter(
            customer=customer,
            otp=entered_otp,
            is_verified=False
        ).order_by("-created_at").first()

        if not otp_record:

            return render(
                request,
                "customers/verify_otp.html",
                {
                    "error": "Invalid OTP. Please try again."
                }
            )

        # --------------------------------
        # Check OTP expiry
        # --------------------------------

        if timezone.now() > otp_record.expires_at:

            return render(
                request,
                "customers/verify_otp.html",
                {
                    "error": "OTP has expired. Please request a new OTP."
                }
            )

        # --------------------------------
        # OTP verified successfully
        # --------------------------------

        otp_record.is_verified = True
        otp_record.save()

        # Login customer
        request.session["customer_id"] = customer.id
        request.session["customer_logged_in"] = True

        # Remove temporary session data
        request.session.pop(
            "login_customer_id",
            None
        )

        return render(
            request,
            "customers/otp_success.html",
            {
                "customer": customer
            }
        )

    # --------------------------------
    # GET request
    # --------------------------------

    return render(
        request,
        "customers/verify_otp.html"
    )


def customer_profile(request):

    customer_id = request.session.get(
        "customer_id"
    )

    if not customer_id:
        return redirect("customer_login")

    customer = Customer.objects.filter(
        id=customer_id
    ).first()

    if not customer:
        return redirect("customer_login")

    return render(
        request,
        "customers/profile.html",
        {
            "customer": customer
        }
    )

def edit_profile(request):

    customer_id = request.session.get(
        "customer_id"
    )

    if not customer_id:
        return redirect("customer_login")

    customer = Customer.objects.filter(
        id=customer_id
    ).first()

    if not customer:
        return redirect("customer_login")

    if request.method == "POST":

        form = CustomerProfileForm(
            request.POST,
            instance=customer
        )

        if form.is_valid():

            form.save()

            return redirect(
                "customer_profile"
            )

    else:

        form = CustomerProfileForm(
            instance=customer
        )

    return render(
        request,
        "customers/edit_profile.html",
        {
            "form": form,
            "customer": customer,
        }
    )
def customer_addresses(request):

    customer_id = request.session.get(
        "customer_id"
    )

    if not customer_id:
        return redirect("customer_login")

    customer = Customer.objects.filter(
        id=customer_id
    ).first()

    if not customer:
        return redirect("customer_login")

    addresses = Address.objects.filter(
        customer=customer
    ).order_by("-created_at")

    return render(
        request,
        "customers/addresses.html",
        {
            "customer": customer,
            "addresses": addresses,
        }
    )