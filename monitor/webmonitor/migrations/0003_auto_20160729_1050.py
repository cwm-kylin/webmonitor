# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webmonitor', '0002_auto_20160727_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hostinfo',
            old_name='ID',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='monitordata',
            old_name='ID',
            new_name='id',
        ),
    ]
