# Generated by Django 4.1.3 on 2022-12-19 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo_app', '0007_details_issue_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountAnn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
