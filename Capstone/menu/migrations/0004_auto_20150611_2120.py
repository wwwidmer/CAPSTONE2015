# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20150609_2231'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('food_type', models.CharField(default=None, max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Category for Food Type',
                'verbose_name': 'Category for Food Type',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('rating', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Rating System',
                'verbose_name': 'Rating System',
            },
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name_plural': 'Menu Management', 'verbose_name': 'Menu Management'},
        ),
        migrations.RenameField(
            model_name='fooditem',
            old_name='menu',
            new_name='menu_title',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='food',
            new_name='food_name',
        ),
        migrations.RemoveField(
            model_name='fooditem',
            name='dishname',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='title',
        ),
        migrations.RemoveField(
            model_name='review',
            name='comment',
        ),
        migrations.AddField(
            model_name='fooditem',
            name='food_name',
            field=models.CharField(default=None, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='menu_title',
            field=models.CharField(default=None, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='menu_title',
            field=models.ForeignKey(default=None, to='menu.Menu'),
        ),
        migrations.AddField(
            model_name='review',
            name='review',
            field=models.TextField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='review',
            name='review_date',
            field=models.DateField(verbose_name='Published on', default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.ForeignKey(default=None, to='menu.Rating'),
        ),
        migrations.AddField(
            model_name='fooditem',
            name='food_type',
            field=models.ForeignKey(default=None, to='menu.FoodType'),
        ),
        migrations.AddField(
            model_name='review',
            name='food_type',
            field=models.ForeignKey(default=None, to='menu.FoodType'),
        ),
    ]
