# Generated by Django 4.0.4 on 2022-07-09 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_alter_categoria_usuario_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tipo_usuario', to='usuarios.categoria_usuario'),
        ),
    ]