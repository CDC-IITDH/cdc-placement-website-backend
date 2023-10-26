# Generated by Django 3.2.13 on 2023-10-26 05:20

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0013_auto_20231022_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalplacement',
            name='allowed_degree',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[['bTech', 'B.Tech'], ['ms/phd', 'MS/ PhD'], ['mTech', 'M.Tech']], max_length=10), default=['bTech'], size=3),
        ),
        migrations.AddField(
            model_name='placement',
            name='allowed_degree',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[['bTech', 'B.Tech'], ['ms/phd', 'MS/ PhD'], ['mTech', 'M.Tech']], max_length=10), default=['bTech'], size=3),
        ),
    ]
