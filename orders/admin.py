from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "customer_name",
        "total_amount",
        "status",
        "payment_status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "session_key",
        "address__full_name",
        "address__phone",
    )

    inlines = [
        OrderItemInline
    ]

    @admin.display(description="Customer")
    def customer_name(self, obj):

        return obj.address.full_name


    @admin.display(description="Payment")
    def payment_status(self, obj):

        if hasattr(obj, "payment"):
            return obj.payment.get_payment_status_display()

        return "No Payment"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product_name",
        "price",
        "quantity",
        "subtotal",
    )

    search_fields = (
        "product_name",
        "order__order_number",
    )