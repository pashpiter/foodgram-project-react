from django.contrib import admin

from user.models import Subscribe, User

from .models import (Ingridient, IngridientInRecipe, IsFavorited,
                     IsInShippingCart, RecipeList, Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name', 'color', 'slug')
    empty_value_display = '-пусто-'


class IngridientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')
    empty_value_display = '-пусто-'


class RecipeListAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'name', 'image', 'text', 'cooking_time'
    )
    search_fields = (
        'author', 'name', 'image', 'text', 'cooking_time'
    )
    list_filter = (
        'author', 'name', 'cooking_time'
    )
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'first_name',
        'last_name', 'role', 'password'
    )
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'subscriber'
    )


class IngridientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'ingridient_in_recipe', 'recipe', 'amount'
    )


class IsIsFavoritedAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'fav_recipe', 'follower'
    )


class IsInShippingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'food_list', 'user_cart'
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingridient, IngridientAdmin)
admin.site.register(RecipeList, RecipeListAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(IngridientInRecipe, IngridientInRecipeAdmin)
admin.site.register(IsFavorited, IsIsFavoritedAdmin)
admin.site.register(IsInShippingCart, IsInShippingCartAdmin)
