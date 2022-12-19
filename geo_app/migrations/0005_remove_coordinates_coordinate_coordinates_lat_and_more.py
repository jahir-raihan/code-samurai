# Generated by Django 4.1.3 on 2022-12-18 02:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('geo_app', '0004_alter_details_completion_percentage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coordinates',
            name='coordinate',
        ),
        migrations.AddField(
            model_name='coordinates',
            name='lat',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coordinates',
            name='lng',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
