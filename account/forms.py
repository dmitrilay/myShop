from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation


class LoginForm(AuthenticationForm, forms.ModelForm):
    username = forms.EmailField()
    username.widget.attrs.update({'class': 'input-base', 'placeholder': 'E-mail'})

    password = forms.CharField(strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'input-base', 'placeholder': 'Пароль'}), )

    class Meta:
        model = User
        fields = ['username', 'password', ]

        # widgets = {
        #     'username': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
        #     # 'password': forms.PasswordInput(attrs={'data-tel-input': '', 'placeholder': 'Телефон'}),
        # }


"""
class LoginForm(forms.Form):
    username = forms.CharField(label='Номер телефона', )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
"""


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    password.widget.attrs.update({'class': 'input-base', 'placeholder': 'Пароль'})
    password2.widget.attrs.update({'class': 'input-base', 'placeholder': 'Повторите пароль'})

    class Meta:
        model = User
        fields = ('email',)

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input-base', 'placeholder': 'E-mail'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароль не совпадает.')
        # return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-base', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'input-base', 'placeholder': 'Фамилия'}),
            'email': forms.TextInput(attrs={'class': 'input-base', 'placeholder': 'E-mail'}), }


class PhoneInput(forms.TextInput):
    input_type = 'tel'


class UserEditPhoneForm(forms.ModelForm, PhoneInput):
    class Meta:
        model = Profile
        fields = ('phone_number', )

        attrs = {'class': 'input-base', 'placeholder': 'Телефон', 'data-tel-input': ''}
        widgets = {'phone_number': PhoneInput(attrs)}


class PasswordResetFormCustom(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': "input-base", 'placeholder': "E-mail"})
    )


class SetPasswordFormCustom(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': "input-base", 'placeholder': 'Пароль'}),
        strip=False, help_text=password_validation.password_validators_help_text_html(),)
    new_password2 = forms.CharField(strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': "input-base", 'placeholder': 'Повторите пароль'}), )


class FavoriteForm(forms.ModelForm):
    class Meta:
        model = FavoriteProduct
        fields = ('id_product', 'title_product', 'profile_favorite')

        widgets = {
            'id_product': forms.TextInput(),
            'title_product': forms.TextInput(),
        }
