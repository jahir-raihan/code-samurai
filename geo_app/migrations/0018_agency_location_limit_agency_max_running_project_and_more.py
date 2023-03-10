# Generated by Django 4.1.3 on 2022-12-21 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geo_app', '0017_proposal_hold'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='location_limit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='agency',
            name='max_running_project',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='agency',
            name='projects_running',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='agency',
            name='spent',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='agency',
            name='yearly_funding',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('count', models.IntegerField(default=0)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo_app.agency')),
            ],
        ),
    ]
