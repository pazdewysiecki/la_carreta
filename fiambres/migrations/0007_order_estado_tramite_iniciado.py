# Generated by Django 4.0.4 on 2022-06-27 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiambres', '0006_alter_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='estado_tramite_iniciado',
            field=models.BooleanField(default=False, verbose_name='Iniciado'),
        ),
    ]