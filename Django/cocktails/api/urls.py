from rest_framework import routers
from cocktails.api.views import CategoryViewSet, CommentViewSet, CocktailViewSet

router = routers.SimpleRouter()
router.register('category', CategoryViewSet)
router.register('comment', CommentViewSet)
router.register('', CocktailViewSet)


urlpatterns = [] + router.urls
