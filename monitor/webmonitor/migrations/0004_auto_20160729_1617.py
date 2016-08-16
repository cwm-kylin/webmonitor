# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webmonitor', '0003_auto_20160729_1050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hostinfo',
            old_name='Alarmconditions',
            new_name='alarmconditions',
        ),
        migrations.RenameField(
            model_name='hostinfo',
            old_name='Alarmtype',
            new_name='alarmtype',
        ),
        migrations.RenameField(
            model_name='hostinfo',
            old_name='AppName',
            new_name='appname',
        ),
        migrations.RenameField(
            model_name='hostinfo',
            old_name='IDC',
            new_name='idc',
        ),
        migrations.RenameField(
            model_name='hostinfo',
            old_name='URL',
            new_name='url',
        ),
    ]
