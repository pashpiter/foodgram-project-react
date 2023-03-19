# Generated by Django 2.2.16 on 2023-03-16 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_isfavorited_isinshippingcart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipelist',
            old_name='ingridietnts',
            new_name='ingridients',
        ),
        migrations.AlterField(
            model_name='ingridient',
            name='measurement_unit',
            field=models.CharField(choices=[('g', 'г'), ('kg', 'кг'), ('ml', 'мл'), ('l', 'л'), ('piece', 'штука')], help_text='Например: кг', max_length=200, verbose_name='Еденицы измерения'),
        ),
    ]