# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0033_auto_20151031_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='csvMembers',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='csvOwners',
        ),
    ]
