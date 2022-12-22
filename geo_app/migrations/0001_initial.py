# Generated by Django 4.1.3 on 2022-12-20 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountAnn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('affiliated_agency', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('project_start_time', models.DateField()),
                ('project_completion_time', models.DateField()),
                ('total_budget', models.IntegerField()),
                ('completion_percentage', models.FloatField()),
                ('issue_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UploadDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.CharField(max_length=200)),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo_app.details')),
            ],
        ),
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lng', models.CharField(max_length=100)),
                ('lat', models.CharField(max_length=100)),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo_app.details')),
            ],
        ),
    ]
