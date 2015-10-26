# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0019_auto_20150507_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiel',
            name='user',
            field=models.OneToOneField(related_name='profiel', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
