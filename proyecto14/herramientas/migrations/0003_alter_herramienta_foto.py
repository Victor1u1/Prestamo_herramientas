# Generated by Django 5.2.2 on 2025-06-05 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herramientas', '0002_herramienta_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='herramienta',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='static/img'),
        ),
    ]
