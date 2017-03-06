# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-02 00:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20170302_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(1, 'Oczekiwanie na realizację'), (2, 'W trakcie realizacji'), (3, 'Gotowe do wysyłki'), (4, 'Wysłano')], max_length=1),
        ),
    ]
