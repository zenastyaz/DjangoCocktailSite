from django import forms

from categories.models import Category
from .models import Cocktail


class CocktailCreateUpdateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Название коктейля"
    }))
    compound = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Название коктейля"
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Описание"
    }))
    ingredient = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Ингредиенты"
    }), required=False)
    cooking_method = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Метод приготовления"
    }), required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(name__in=["Алкогольные", "Безалкогольные"]),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Выберите категорию",
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            "class": "form-control",
            "placeholder": "Выберите изображение"
        }), required=False)
    image_url = forms.URLField(
        widget=forms.URLInput(attrs={
            "class": "form-control",
            "placeholder": "http://...",
        }), required=False)

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')

        if not image and not image_url:
            raise forms.ValidationError('Необходимо загрузить изображение или указать ссылку на него.')

        return cleaned_data

    class Meta:
        model = Cocktail
        fields = ['name', 'compound', 'description', 'ingredient', 'cooking_method', 'image', 'image_url']
