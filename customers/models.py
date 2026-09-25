from django.db import models


class Customer(models.Model):

    email = models.EmailField(
        unique=True,
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    full_name = models.CharField(
        max_length=200,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        if self.full_name:
            return self.full_name

        if self.phone:
            return self.phone

        return self.email


class Address(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="addresses",
        null=True,
        blank=True
    )

    session_key = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    full_name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=20
    )

    address_line_1 = models.CharField(
        max_length=255
    )

    address_line_2 = models.CharField(
        max_length=255,
        blank=True
    )

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    postal_code = models.CharField(
        max_length=20
    )

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

class OTPVerification(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="otp_verifications"
    )

    otp = models.CharField(
        max_length=6
    )

    is_verified = models.BooleanField(
        default=False
    )

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.customer} - {self.otp}"