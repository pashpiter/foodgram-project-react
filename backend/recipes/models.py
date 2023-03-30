from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from user.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text='Например: Завтрак',
        verbose_name='Название'
    )
    color = models.CharField(
        null=True,
        blank=True,
        unique=True,
        max_length=7,
        help_text='Например: #E26C2D',
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        null=True,
        blank=True,
        unique=True,
        max_length=200,
        help_text='Например: breakfast',
        verbose_name='Уникальный слаг',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text='Например: Капуста',
        verbose_name='Название ингридиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        help_text='Например: кг',
        verbose_name='Еденицы измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class RecipeList(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Тэги'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipe_ingredients',
        verbose_name='Ингридиенты',
        through='IngredientInRecipe',
    )
    name = models.CharField(
        max_length=200,
        help_text='Например: Яичница',
        verbose_name='Название рецепта',
        unique=True
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipes/',
    )
    text = models.TextField(
        help_text='Описание рецепта',
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveIntegerField(
        help_text='Время приготовления в минутах (минимум 1 минута)',
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                1, 'Время приготовления не может быть меньше минуты'
            ),
            MaxValueValidator(
                300, 'Время приготовления не может быть больше 5 часов'
            )
        ]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id', )

    def __str__(self):
        return f'{self.name}'


class IngredientInRecipe(models.Model):
    ingredient_in_recipe = models.ForeignKey(
        Ingredient,
        related_name='in_ingredient',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        RecipeList,
        related_name='in_recipe',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        help_text='Например: 1',
        validators=[
            MinValueValidator(
                1, 'Количество не может быть меньше 1'
            ),
            MaxValueValidator(
                10000, 'Количество не может быть больше 10000'
            )
        ]
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class IsFavorited(models.Model):
    fav_recipe = models.ForeignKey(
        RecipeList,
        related_name='fav_recipe',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    follower = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('fav_recipe',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class IsInShippingCart(models.Model):
    food_list = models.ForeignKey(
        RecipeList,
        related_name='food_list',
        verbose_name='Список продуктов из рецепта',
        on_delete=models.CASCADE
    )
    user_cart = models.ForeignKey(
        User,
        related_name='user_cart',
        verbose_name='Пользователь корзины',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('user_cart',)
        verbose_name = 'Покупательская корзина'
        verbose_name_plural = 'Покупательская корзина'
