from rest_framework import routers
from cocktails.api.views import CategoryViewSet, CommentViewSet, CocktailViewSet, FavoriteViewSet

router = routers.SimpleRouter()
router.register('category', CategoryViewSet)
router.register('comment', CommentViewSet)
router.register('favorite', FavoriteViewSet)
router.register('', CocktailViewSet)


urlpatterns = [] + router.urls
