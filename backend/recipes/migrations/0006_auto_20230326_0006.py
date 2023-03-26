# Generated by Django 2.2.16 on 2023-03-26 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20230321_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingridient',
            name='measurement_unit',
            field=models.CharField(choices=[('g', 'г'), ('kg', 'кг'), ('ml', 'мл'), ('l', 'л'), ('piece', 'штука'), ('random', 'по вкусу')], help_text='Например: кг', max_length=200, verbose_name='Еденицы измерения'),
        ),
    ]
