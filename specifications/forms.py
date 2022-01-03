from django import forms
from .models import CategoryProducts


class NewCategoryFeatureKeyForm(forms.ModelForm):
    class Meta:
        model = CategoryProducts
        fields = ('name_cat',)

        widgets = {
            'name_cat': forms.TextInput(attrs={'class': 'form-control'}),
        }
