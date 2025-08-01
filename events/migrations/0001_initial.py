# Generated by Django 5.2.4 on 2025-07-27 03:41

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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=255)),
                ('asset', models.ImageField(blank=True, null=True, upload_to='event_asset/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.category')),
                ('participants', models.ManyToManyField(blank=True, related_name='rsvped_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
