# Generated by Django 2.2.16 on 2023-03-27 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20230327_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipelist',
            name='image',
            field=models.ImageField(help_text='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB', upload_to='', verbose_name='Ссылка на картинку готового блюда на сайте'),
        ),
    ]
