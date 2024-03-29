# Generated by Django 4.1.5 on 2023-04-27 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travel', '0003_travel_agency'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='travel_agency',
            options={'ordering': ['-time_create', 'title'], 'verbose_name': 'Тур агенттік', 'verbose_name_plural': 'Тур агенттіктер'},
        ),
        migrations.AlterField(
            model_name='travel_agency',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Tour Agency'),
        ),
        migrations.AlterField(
            model_name='travel_agency',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пайдаланушы'),
        ),
    ]
