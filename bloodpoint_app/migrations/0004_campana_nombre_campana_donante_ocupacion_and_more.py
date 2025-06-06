# Generated by Django 5.2 on 2025-06-03 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodpoint_app', '0003_alter_customuser_email_alter_customuser_rut_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campana',
            name='nombre_campana',
            field=models.CharField(default='Campana Cruz Roja', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donante',
            name='ocupacion',
            field=models.CharField(default='Otro', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='donacion',
            name='tipo_donacion',
            field=models.CharField(choices=[('campana', 'Campaña'), ('solicitud', 'Solicitud de Campaña')], max_length=20),
        ),
    ]
