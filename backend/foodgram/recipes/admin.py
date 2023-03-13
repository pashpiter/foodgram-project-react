from django.contrib import admin

from .models import Tag, Ingridient, RecipeList
from user.models import User


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
        'id', 'author', 'name', 'image', 'text',
        'is_favorited', 'is_in_shopping_cart', 'cooking_time'
    )
    search_fields = (
        'author', 'name', 'image', 'text',
        'is_favorited', 'is_in_shopping_cart', 'cooking_time'
    )
    list_filter = (
        'author', 'name', 'cooking_time'
    )
    empty_value_display = '-пусто-'

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'first_name', 'last_name', 'role', 'password'
    )
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingridient, IngridientAdmin)
admin.site.register(RecipeList, RecipeListAdmin)
admin.site.register(User, UserAdmin)