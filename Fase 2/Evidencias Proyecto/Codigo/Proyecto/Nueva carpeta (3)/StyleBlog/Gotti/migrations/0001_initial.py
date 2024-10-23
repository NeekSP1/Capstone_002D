# Generated by Django 5.1.2 on 2024-10-20 01:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatosPersonales',
            fields=[
                ('idDatoPersonal', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('contraseña', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=255)),
                ('correoElectronico', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Barbero',
            fields=[
                ('datospersonales_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='Gotti.datospersonales')),
                ('idBarbero', models.AutoField(primary_key=True, serialize=False)),
                ('especialidad', models.CharField(max_length=100)),
                ('horario', models.DateField()),
            ],
            bases=('Gotti.datospersonales',),
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('datospersonales_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='Gotti.datospersonales')),
                ('idCliente', models.AutoField(primary_key=True, serialize=False)),
                ('telefono', models.CharField(max_length=15)),
            ],
            bases=('Gotti.datospersonales',),
        ),
    ]
