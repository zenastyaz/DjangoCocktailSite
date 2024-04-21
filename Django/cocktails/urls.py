from django.urls import path, include
import debug_toolbar

from .views import (
    CocktailListView,
    CocktailCreateView,
    CocktailUpdateView,
    MyCocktailListView,
    CocktailDet,
    add_like,
    MyFavouriteCocktails,
    archive,
    add_comment,
    delete_comment
)


urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('', CocktailListView.as_view(), name='cocktail-list'),
    path('create', CocktailCreateView.as_view(), name='cocktail-create'),
    path('<int:pk>/update', CocktailUpdateView.as_view(), name='update-cocktail'),
    path('mycockt', MyCocktailListView.as_view(), name='my-cocktail'),
    path('<int:pk>/coctail', CocktailDet.as_view(), name='cocktail'),
    path('favorite', MyFavouriteCocktails.as_view(), name='cocktail-favorite'),
    path('<int:pk>/like', add_like, name='cocktail-like'),
    path('<int:pk>/archive', archive, name='archive_cocktail'),
    path('<int:pk>/add-comment/', add_comment, name='add-comment'),
    path('<int:pk>/delete_comment/', delete_comment, name='delete-comment'),
]
