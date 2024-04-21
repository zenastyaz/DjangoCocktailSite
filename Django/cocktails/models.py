from django.db import models


class Cocktail(models.Model):
    name = models.CharField(max_length=100)
    compound = models.TextField(blank=True)
    ingredient = models.TextField(blank=True)
    cooking_method = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='cocktails_images/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    creator = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='created_cocktails')
    my_favorites = models.ManyToManyField('users.User', through='cocktails.Favorite', related_name='liked_by')
    category = models.ForeignKey('categories.Category', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='cocktails')
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    cocktail = models.ForeignKey('cocktails.Cocktail', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField(blank=False)
    creator = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='created_comments')
    date = models.DateTimeField(auto_now_add=True)
    cocktail = models.ForeignKey('cocktails.Cocktail', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
