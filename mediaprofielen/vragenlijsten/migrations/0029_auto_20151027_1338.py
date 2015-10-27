# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0028_remove_enqueteanswer_enquete'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='color',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='invulmoment',
            name='organisation',
            field=models.ForeignKey(related_name='organisationinvulmoment', to='vragenlijsten.Organisation'),
        ),
    ]
