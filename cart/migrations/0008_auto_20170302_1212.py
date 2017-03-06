# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-02 11:12
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_auto_20170302_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Ilość'),
        ),
    ]
