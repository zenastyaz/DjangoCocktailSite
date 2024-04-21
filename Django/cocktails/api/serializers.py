from rest_framework import serializers
from cocktails.models import Cocktail, Comment
from categories.models import Category


class CommentSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(read_only=True)
    cocktail_name = serializers.SerializerMethodField(read_only=True)
    cocktail = serializers.PrimaryKeyRelatedField(queryset=Cocktail.objects.all(), required=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "cocktail",
            "cocktail_name",
            "parent",
            "creator",
            "text",
            "date",
        ]

    def get_cocktail_name(self, obj):
        return obj.cocktail.name if obj.cocktail else None

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
        ]


class CocktailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    image_url = serializers.URLField(required=False)

    class Meta:
        model = Cocktail
        fields = [
            "id",
            "name",
            "compound",
            "image",
            "image_url",
            "creator",
            "is_archived",
        ]


class CocktailsDetailSerializer(CocktailSerializer):

    class Meta:
        model = Cocktail
        fields = CocktailSerializer.Meta.fields + [
            "ingredient",
            "cooking_method",
            "description",
            "my_favorites",
            "category",
        ]
