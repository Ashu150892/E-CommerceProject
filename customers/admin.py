from django.contrib import admin

from .models import Customer, Address, OTPVerification


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "email",
        "phone",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "full_name",
        "email",
        "phone",
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "phone",
        "city",
        "state",
        "postal_code",
        "country",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "city",
        "postal_code",
    )


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):

    list_display = (
        "customer",
        "otp",
        "is_verified",
        "expires_at",
        "created_at",
    )

    list_filter = (
        "is_verified",
        "created_at",
    )

    search_fields = (
        "customer__email",
        "customer__phone",
        "otp",
    )