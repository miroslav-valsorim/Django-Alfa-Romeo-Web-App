# Generated by Django 5.0.3 on 2024-03-18 08:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_alfaromeouser_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='alfaromeouser',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='date joined'),
        ),
    ]
