from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

from user.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Например: Завтрак',
        verbose_name='Название'
    )
    color = models.CharField(
        null=True,
        blank=True,
        max_length=7,
        help_text='Например: #E26C2D',
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        null=True,
        blank=True,
        max_length=200,
        help_text='Например: breakfast',
        verbose_name='Уникальный слаг',
    )

class Ingridient(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Например: Капуста',
        verbose_name='Название ингридиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        help_text='Например: кг',
        verbose_name='Еденицы измерения'
    )

class RecipeList(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Тэги'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта'
    )
    ingridietnts = models.ManyToManyField(
        Ingridient,
        related_name='ingridients',
        verbose_name='Ингридиенты'
    )
    def is_favorited(self):
        pass

    def is_in_shopping_cart(self):
        pass

    name = models.CharField(
        max_length=200,
        help_text='Например: Яичница',
        verbose_name='Название рецепта'
    )
    image = models.URLField(
        help_text='Например: http://foodgram.example.org/media/recipes/'
        'images/image.jpeg',
        verbose_name='Ссылка на картинку готового блюда на сайте'
    )
    text = models.CharField(
        help_text='Описание рецепта',
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveIntegerField(
        help_text='Время приготовления в минутах (минимум 1 минута)',
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(1, 'Время приготовления не может быть меньше '
                                 'минуты')
        ]
    )
