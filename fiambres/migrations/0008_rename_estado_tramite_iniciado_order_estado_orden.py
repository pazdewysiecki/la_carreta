# Generated by Django 4.0.4 on 2022-06-27 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fiambres', '0007_order_estado_tramite_iniciado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='estado_tramite_iniciado',
            new_name='estado_orden',
        ),
    ]
