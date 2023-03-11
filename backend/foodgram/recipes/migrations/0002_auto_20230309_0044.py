# Generated by Django 2.2.16 on 2023-03-08 21:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipelist',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AddField(
            model_name='recipelist',
            name='ingridietnts',
            field=models.ManyToManyField(related_name='ingridients', to='recipes.Ingridient', verbose_name='Ингридиенты'),
        ),
        migrations.AddField(
            model_name='recipelist',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='recipes.Tag', verbose_name='Тэги'),
        ),
    ]