# Generated by Django 5.2 on 2025-06-17 05:46

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bloodpoint_app', '0007_respuestas_representante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='representante_org',
            name='credencial',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='image'),
        ),
    ]
