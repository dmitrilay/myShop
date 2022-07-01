from django import forms
from .models import Order
from django.forms.widgets import TextInput


class PhoneInput(TextInput):
    input_type = 'tel'


class OrderCreateForm(forms.ModelForm, PhoneInput):

    class Meta:
        model = Order
        fields = ['email', 'phone_number', ]
        # fields = ['first_name', 'email', 'phone_number', ]

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            'phone_number': PhoneInput(attrs={'data-tel-input': '', 'placeholder': 'Телефон'}),
        }

# class PhoneInput(TextInput):
#     input_type = 'tel'


# class OrderCreateForm(forms.Form, PhoneInput):
#     attrs_email = {'placeholder': 'email'}
#     email = forms.EmailField(widget=forms.TextInput(attrs=attrs_email))

#     attrs_tel = {'data-tel-input': '', 'placeholder': 'Телефон'}
#     phone_number = forms.IntegerField(widget=PhoneInput(attrs=attrs_tel))
