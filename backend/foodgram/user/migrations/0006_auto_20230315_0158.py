# Generated by Django 2.2.16 on 2023-03-15 01:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_subscribe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribe',
            name='subscriber',
        ),
        migrations.AddField(
            model_name='subscribe',
            name='subscriber',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL, verbose_name='Сабскрайбер'),
            preserve_default=False,
        ),
    ]