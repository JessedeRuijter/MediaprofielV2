# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0031_auto_20151027_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiel',
            name='time',
            field=models.DateField(),
        ),
    ]
