# Generated by Django 3.2.21 on 2023-09-14 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_publicaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicaciones',
            name='comentarios',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
