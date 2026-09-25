from django import forms
from .models import Address


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address

        fields = [
            "full_name",
            "phone",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "country",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "placeholder": "Full Name"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Phone Number"
                }
            ),

            "address_line_1": forms.TextInput(
                attrs={
                    "placeholder": "Address Line 1"
                }
            ),

            "address_line_2": forms.TextInput(
                attrs={
                    "placeholder": "Address Line 2"
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "placeholder": "City"
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "placeholder": "State"
                }
            ),

            "postal_code": forms.TextInput(
                attrs={
                    "placeholder": "Postal Code"
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "placeholder": "Country"
                }
            ),
        }