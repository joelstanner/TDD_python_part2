# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_item_list'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='List',
            new_name='TodoList',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='list',
            new_name='todo_list',
        ),
    ]
