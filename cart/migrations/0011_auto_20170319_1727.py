# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-19 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data'),
        ),
    ]
