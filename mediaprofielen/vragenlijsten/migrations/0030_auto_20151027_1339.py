# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0029_auto_20151027_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='color',
            field=models.CharField(max_length=100),
        ),
    ]
