# Generated by Django 4.0.4 on 2022-06-26 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiambres', '0004_remove_order_paid_status_alter_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
