from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

from user.models import User

MEASURMENT_UNI_CHOICES = (
    ('g', 'г'), ('kg', 'кг'), ('ml', 'мл'), ('l', 'л'), ('piece', 'штука')
)

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

    def __str__(self):
        return f'{self.name}'

class Ingridient(models.Model):
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
        choices=MEASURMENT_UNI_CHOICES
    )

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
    ingridients = models.ManyToManyField(
        Ingridient,
        related_name='recipe_ingridients',
        verbose_name='Ингридиенты',
        through='IngridientInRecipe',
    )
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
            )
        ]
    )

    def __str__(self):
        return f'{self.name}'

class IngridientInRecipe(models.Model):
    ingridients = models.ForeignKey(
        Ingridient,
        related_name='in_ingridients',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        RecipeList,
        related_name='in_recipe',
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        verbose_name='количество',
        help_text='Например: 1'
    )

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