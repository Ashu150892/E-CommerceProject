from django.contrib import admin
from .models import Address


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