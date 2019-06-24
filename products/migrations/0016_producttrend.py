# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTrend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'products/')),
                ('product', models.ForeignKey(to='products.Product')),
            ],
        ),
    ]
