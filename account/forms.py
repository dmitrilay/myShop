from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm, forms.ModelForm):
    username = forms.CharField(label='Email или номер телефона', )

    class Meta:
        model = User
        fields = ('username', 'password',)


"""
class LoginForm(forms.Form):
    username = forms.CharField(label='Номер телефона', )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
"""


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    password.widget.attrs.update({'class': 'form-control'})
    password2.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            "username": "Номер телефона",
        }
        exclude = ['first_name', ]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароль не совпадает.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

        widgets = {
            # 'date_of_birth': forms.TextInput(),
            'date_of_birth': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

        labels = {
            "date_of_birth": "Дата рождения",
            "photo": "Фото",
        }
