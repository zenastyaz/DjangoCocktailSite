import django_filters
from django import forms

from cocktails.models import Cocktail
from categories.models import Category


class FilteredCocktails(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'name'}))
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.filter(name__in=["Алкогольные", "Безалкогольные"]),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Cocktail
        fields = ['name', 'category']