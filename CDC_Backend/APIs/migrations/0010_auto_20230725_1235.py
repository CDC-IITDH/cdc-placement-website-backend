# Generated by Django 3.2.13 on 2023-07-25 07:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0009_auto_20230725_0254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalinternship',
            name='season',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[['Summer', 'Summer'], ['Winter', 'Winter'], ['Autumn', 'Autumn'], ['Spring', 'Spring']], max_length=10), default=list, size=4),
        ),
        migrations.AlterField(
            model_name='internship',
            name='season',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[['Summer', 'Summer'], ['Winter', 'Winter'], ['Autumn', 'Autumn'], ['Spring', 'Spring']], max_length=10), default=list, size=4),
        ),
    ]
