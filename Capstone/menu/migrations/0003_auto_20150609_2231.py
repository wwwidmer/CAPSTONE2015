# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20150609_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='menu',
            field=models.ForeignKey(to='menu.Menu', default=None),
        ),
        migrations.AddField(
            model_name='review',
            name='food',
            field=models.ForeignKey(to='menu.FoodItem', default=None),
        ),
    ]
