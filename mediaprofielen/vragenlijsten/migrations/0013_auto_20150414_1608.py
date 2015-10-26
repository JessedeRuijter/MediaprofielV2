# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0012_auto_20150414_1555'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profiel',
            old_name='completedBlocks',
            new_name='completedEnquetes',
        ),
    ]
