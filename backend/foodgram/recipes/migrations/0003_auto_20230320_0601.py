# Generated by Django 2.2.16 on 2023-03-20 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20230320_0352'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingridientinrecipe',
            old_name='ingridient',
            new_name='ingridient_in_recipe',
        ),
    ]