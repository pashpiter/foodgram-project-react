# Generated by Django 2.2.16 on 2023-03-30 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('-id',), 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('id',), 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
    ]