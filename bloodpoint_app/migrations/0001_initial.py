# Generated by Django 5.2 on 2025-04-19 01:01

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='adminbp',
            fields=[
                ('id_admin', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField()),
                ('email', models.EmailField(max_length=254)),
                ('contrasena', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='centro_donacion',
            fields=[
                ('id_centro', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_centro', models.CharField()),
                ('direccion_centro', models.CharField()),
                ('comuna', models.CharField()),
                ('telefono', models.CharField()),
                ('fecha_creacion', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='representante_org',
            fields=[
                ('id_representante', models.AutoField(primary_key=True, serialize=False)),
                ('rol', models.CharField()),
                ('nombre', models.CharField()),
                ('email', models.EmailField(max_length=254)),
                ('contrasena', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('test_field', models.CharField(blank=True, max_length=50, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='donante',
            fields=[
                ('id_donante', models.AutoField(primary_key=True, serialize=False)),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('nombre_completo', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=255)),
                ('comuna', models.CharField(max_length=100)),
                ('fono', models.CharField(max_length=20)),
                ('fecha_nacimiento', models.DateField()),
                ('nacionalidad', models.CharField(max_length=50)),
                ('tipo_sangre', models.CharField(choices=[('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=3)),
                ('dispo_dia_donacion', models.CharField(max_length=50)),
                ('nuevo_donante', models.BooleanField(default=False)),
                ('noti_emergencia', models.BooleanField(default=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='donacion',
            fields=[
                ('id_donacion', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_donacion', models.DateField()),
                ('cantidad_donacion', models.IntegerField()),
                ('centro_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloodpoint_app.centro_donacion')),
                ('id_donante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloodpoint_app.donante')),
            ],
        ),
        migrations.CreateModel(
            name='logro',
            fields=[
                ('id_logro', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion_logro', models.CharField()),
                ('fecha_logro', models.DateField()),
                ('id_donante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloodpoint_app.donante')),
            ],
        ),
        migrations.AddField(
            model_name='centro_donacion',
            name='id_representante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloodpoint_app.representante_org'),
        ),
        migrations.CreateModel(
            name='campana',
            fields=[
                ('id_campana', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_campana', models.DateField()),
                ('apertura', models.TimeField()),
                ('cierre', models.TimeField()),
                ('meta', models.CharField()),
                ('latitud', models.CharField()),
                ('longitud', models.CharField()),
                ('id_centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloodpoint_app.centro_donacion')),
                ('id_representante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloodpoint_app.representante_org')),
            ],
        ),
        migrations.CreateModel(
            name='solicitud_campana_repo',
            fields=[
                ('id_solicitud', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_sangre_sol', models.CharField()),
                ('fecha_solicitud', models.DateField()),
                ('cantidad_personas', models.IntegerField()),
                ('descripcion_solicitud', models.CharField()),
                ('direccion_solicitud', models.CharField()),
                ('comuna_solicitud', models.CharField()),
                ('latitud', models.CharField()),
                ('longitud', models.CharField()),
                ('id_donante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloodpoint_app.donante')),
            ],
        ),
    ]
