# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webmonitor', '0005_auto_20160729_1626'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monitorappinfo',
            old_name='idc',
            new_name='isp',
        ),
        migrations.AlterField(
            model_name='monitorappinfo',
            name='appname',
            field=models.CharField(unique=True, max_length=40),
        ),
    ]
