# Generated by Django 3.2.13 on 2023-10-21 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0012_auto_20231010_0046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalstudent',
            name='can_apply',
        ),
        migrations.RemoveField(
            model_name='student',
            name='can_apply',
        ),
        migrations.AddField(
            model_name='historicalstudent',
            name='can_apply_placements',
            field=models.BooleanField(default=True, verbose_name='Placement_Registered'),
        ),
        migrations.AddField(
            model_name='student',
            name='can_apply_placements',
            field=models.BooleanField(default=True, verbose_name='Placement_Registered'),
        ),
    ]