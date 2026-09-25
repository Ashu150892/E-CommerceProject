from django.db import models


class Address(models.Model):

    session_key = models.CharField(
    max_length=100,
    blank=True,
    null=True
)

    full_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    address_line_1 = models.CharField(max_length=255)

    address_line_2 = models.CharField(
        max_length=255,
        blank=True
    )

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    postal_code = models.CharField(max_length=20)

    country = models.CharField(
        max_length=100,
        default="India"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.full_name} - {self.city}"