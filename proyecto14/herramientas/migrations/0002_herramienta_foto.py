# Generated by Django 5.2.2 on 2025-06-05 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herramientas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='herramienta',
            name='foto',
            field=models.ImageField(null=True, upload_to='static/img'),
        ),
    ]
