from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 4)]


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='Количество', widget=forms.TextInput(
        attrs={'class': 'quantity-pr__input', 'value': '1', 'readonly': ''}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


# name = forms.CharField()
