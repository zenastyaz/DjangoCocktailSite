from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from cocktails.api.serializers import (
    CategorySerializer,
    CommentSerializer,
    CocktailSerializer,
    CocktailsDetailSerializer
)
from categories.models import Category
from cocktails.models import Comment, Cocktail
from rest_framework import mixins


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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
        queryset = queryset.filter(is_archived=True)
        return queryset

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
