# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-07 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0004_auto_20170321_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tier',
            name='name',
            field=models.CharField(choices=[('trial', 'Trial'), ('basic', 'Basic'), ('pro', 'Professional'), ('premium', 'Premium')], default='trial', max_length=255),
        ),
    ]
