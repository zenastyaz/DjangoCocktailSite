from django.contrib import admin
from cocktails.models import Cocktail, Favorite

admin.site.register(Cocktail)
admin.site.register(Favorite)
