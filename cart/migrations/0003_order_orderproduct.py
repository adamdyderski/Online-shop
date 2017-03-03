# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-01 21:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0006_auto_20170226_2201'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0002_auto_20170226_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Kwota zamówienia')),
                ('shipping_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.ShippingMethod', verbose_name='Sposób wysyłki')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik')),
            ],
            options={
                'verbose_name_plural': 'Zamówienia',
                'verbose_name': 'Zamówienie',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Ilość')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.Order', verbose_name='Zamówienie')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_app.Product', verbose_name='Produkt')),
            ],
            options={
                'verbose_name_plural': 'Zamówione produkty',
                'verbose_name': 'Zamówiony produkt',
            },
        ),
    ]
