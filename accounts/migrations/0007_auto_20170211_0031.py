# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-10 23:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20170210_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Telefon'),
        ),
        migrations.AlterField(
            model_name='user',
            name='postcode',
            field=models.CharField(max_length=6, verbose_name='Kod pocztowy'),
        ),
    ]