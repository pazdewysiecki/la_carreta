# Generated by Django 4.0.4 on 2022-07-15 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_alter_usuario_tipo_usuario'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoria_usuario',
            options={'ordering': ['id'], 'verbose_name': 'Categoria_Usuario', 'verbose_name_plural': 'Categoria_Usuarios'},
        ),
        migrations.AlterModelTable(
            name='categoria_usuario',
            table='Categoria_Usuario',
        ),
    ]
