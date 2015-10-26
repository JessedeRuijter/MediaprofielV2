# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0014_profiletext'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiletext',
            name='profiel',
            field=models.CharField(default='GE', max_length=b'2', choices=[(b'GE', b'Geen profiel'), (b'Co', b'Consument'), (b'Ve', b'Verzamelaar'), (b'St', b'Strateeg'), (b'Ne', b'Netwerker'), (b'On', b'Ontwerper')]),
            preserve_default=False,
        ),
    ]
