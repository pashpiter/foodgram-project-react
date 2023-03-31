from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import (
    ModelChoiceFilter,
    AllValuesMultipleFilter,
    BooleanFilter
)

from recipes.models import RecipeList
from user.models import User


class TagAuthorFavoriteCartFilter(FilterSet):
    author = ModelChoiceFilter(queryset=User.objects.all())
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = BooleanFilter(method='is_favorite_filter')
    is_in_shopping_cart = BooleanFilter(method='is_in_shopping_cart_filter')

    def is_favorite_filter(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(baskets__user=self.request.user)
        return queryset

    class Meta:
        model = RecipeList
        fields = ('tags', 'author')
