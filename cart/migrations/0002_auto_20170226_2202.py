# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-26 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingmethod',
            name='days',
            field=models.IntegerField(verbose_name='Przewidywany czas dostawy (dni)'),
        ),
    ]