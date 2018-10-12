# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_productfeatured'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCharged',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveIntegerField()),
                ('source', models.CharField(max_length=100)),
                ('currency', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500, null=True, blank=True)),
            ],
        ),
    ]
