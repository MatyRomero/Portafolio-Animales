# Generated by Django 3.2.22 on 2023-11-26 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20231124_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='similitud',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='similitud',
            name='similitud',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
