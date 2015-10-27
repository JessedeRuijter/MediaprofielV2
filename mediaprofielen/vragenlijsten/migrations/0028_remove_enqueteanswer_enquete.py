# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0027_profiel_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enqueteanswer',
            name='enquete',
        ),
    ]
