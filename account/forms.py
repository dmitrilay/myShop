from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm


class LoginForm(AuthenticationForm, forms.ModelForm):
    username = forms.CharField()
    username.widget.attrs.update({'class': 'input-base', 'placeholder': 'E-mail'})

    password = forms.CharField()
    password.widget.attrs.update({'class': 'input-base', 'placeholder': 'Пароль'})

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
