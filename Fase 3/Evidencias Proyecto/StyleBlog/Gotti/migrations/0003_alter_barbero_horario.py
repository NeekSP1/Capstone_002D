# Generated by Django 5.1.2 on 2024-11-25 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gotti', '0002_alter_barberopendiente_horario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barbero',
            name='horario',
            field=models.DateField(null=True),
        ),
    ]