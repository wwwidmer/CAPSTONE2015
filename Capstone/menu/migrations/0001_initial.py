# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractMenuItem',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('logo', models.ImageField(upload_to='media', blank=True, verbose_name='logo')),
                ('dishName', models.CharField(max_length=30)),
                ('average', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('type', models.CharField(default=None, max_length=30)),
            ],
            options={
                'verbose_name': 'Category for Food Type',
                'verbose_name_plural': 'Category for Food Type',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(default=None, max_length=30)),
                ('logo', models.ImageField(upload_to='media', blank=True, verbose_name='logo')),
            ],
            options={
                'verbose_name': 'Menu Management',
                'verbose_name_plural': 'Menu Management',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('createdBy', models.CharField(default='No one', max_length=30)),
                ('logo', models.ImageField(upload_to='media', blank=True, verbose_name='logo')),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('createdOn', models.DateField(verbose_name='Published on')),
                ('reviewComment', models.TextField(default=None, max_length=200)),
                ('foodItemName', models.ForeignKey(default=None, to='menu.FoodItem', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='fooditem',
            name='menuName',
            field=models.ForeignKey(default=None, to='menu.Menu'),
        ),
        migrations.AddField(
            model_name='fooditem',
            name='type',
            field=models.ForeignKey(default=None, to='menu.FoodType'),
        ),
    ]
