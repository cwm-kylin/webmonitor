# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webmonitor', '0004_auto_20160729_1617'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Hostinfo',
            new_name='MonitorAppInfo',
        ),
    ]
