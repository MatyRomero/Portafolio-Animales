# Generated by Django 3.2.22 on 2023-11-28 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20231126_0001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='similitud',
            name='publicacion',
        ),
        migrations.AddField(
            model_name='similitud',
            name='publicacion_comparada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='similitudes_comparadas', to='core.publicaciones'),
        ),
        migrations.AddField(
            model_name='similitud',
            name='publicacion_usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='similitudes_usuario', to='core.publicaciones'),
        ),
    ]
