# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 23:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_divisible', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('manufacturer', models.ManyToManyField(related_name='manufacturers', to='parts.Manufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='SubPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='parts.Part')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='parts.Part')),
            ],
        ),
        migrations.AddField(
            model_name='part',
            name='subpart',
            field=models.ManyToManyField(related_name='subparts', through='parts.SubPart', to='parts.Part'),
        ),
        migrations.AddField(
            model_name='cost',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='costs', to='parts.Part'),
        ),
    ]
