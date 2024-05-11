from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from cocktails.api.serializers import (
    CategorySerializer,
    CommentSerializer,
    CocktailSerializer,
    CocktailsDetailSerializer,
    FavoritesSerializer,
)
from categories.models import Category
from cocktails.models import Comment, Cocktail, Favorite
from rest_framework import mixins, status


class CategoryViewSet(mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CocktailViewSet(ModelViewSet):
    queryset = Cocktail.objects.all()
    serializer_class = CocktailSerializer

    def get_serializer_class(self):
        if self.detail:
            return CocktailsDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in 'archive':
            return queryset
        return queryset.filter(is_archived=False)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        user = request.user
        cocktail_id = pk
        favorite, created = Favorite.objects.get_or_create(
            cocktail_id=cocktail_id,
            user=user
        )
        if not created:
            favorite.delete()
            return Response({'liked': False}, status=status.HTTP_200_OK)

        return Response({'liked': True}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def archive(self, request, pk=None):
        user = request.user
        cocktail = self.get_object()
        action = request.data.get('action', 'archive')

        if action == 'archive':
            cocktail.is_archived = True
        elif action == 'off_archive':
            cocktail.is_archived = False
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        cocktail.save()
        return Response({'archive': cocktail.is_archived}, status=status.HTTP_200_OK)


class FavoriteViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(methods=['get'], detail=False)
    def favorites(self, request):
        cocktail_id = request.query_params.get('cocktail_id')
        if cocktail_id:
            queryset = Favorite.objects.filter(cocktail_id=cocktail_id, user=request.user)
            serializer = FavoritesSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"error": "No cocktail_id provided"}, status=status.HTTP_400_BAD_REQUEST)
