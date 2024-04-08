# Generated by Django 5.0.3 on 2024-04-08 13:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MuseumCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('img_field', models.ImageField(upload_to='museum_gallery/')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Museum Categories',
            },
        ),
        migrations.CreateModel(
            name='MuseumTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=150)),
                ('img_field', models.ImageField(blank=True, null=True, upload_to='museum_gallery/')),
                ('description', models.TextField()),
                ('year', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='museum.museumcategory')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topic_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Museum Topics',
            },
        ),
    ]
