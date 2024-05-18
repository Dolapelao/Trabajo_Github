# Generated by Django 4.2.5 on 2024-05-18 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_actividad_actividade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('asunto', models.CharField(max_length=250)),
                ('mensaje', models.TextField()),
            ],
        ),
    ]
