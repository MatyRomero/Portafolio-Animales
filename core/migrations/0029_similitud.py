# Generated by Django 3.2.22 on 2023-11-14 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_publicaciones_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Similitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similitud', models.FloatField()),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.publicaciones')),
            ],
        ),
    ]
