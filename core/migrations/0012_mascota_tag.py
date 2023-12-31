# Generated by Django 3.2.19 on 2023-10-04 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20231003_2237'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('es_animal', models.BooleanField(choices=[(True, 'Sí'), (False, 'No')], default=True)),
                ('tipo_de_animal', models.CharField(max_length=255)),
                ('color', models.TextField()),
                ('tags', models.ManyToManyField(to='core.Tag')),
            ],
        ),
    ]
