from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name',
                  'email',
                  'phone_number',
                  # 'profile',
                  ]
        # exclude = ['profile', ]

        labels = {
            "first_name": "Ваше имя",
            "phone_number": "Номер телефона",
        }

