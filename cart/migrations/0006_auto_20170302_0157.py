# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-02 00:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_auto_20170302_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Oczekiwanie na realizację'), (2, 'W trakcie realizacji'), (3, 'Gotowe do wysyłki'), (4, 'Wysłano')], default=1),
        ),
    ]