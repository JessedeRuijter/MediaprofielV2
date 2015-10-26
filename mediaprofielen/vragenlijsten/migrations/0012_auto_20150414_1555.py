# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0011_question_profiel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answers',
            field=models.CharField(max_length=1000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='profiel',
            field=models.CharField(max_length=b'2', choices=[(b'GE', b'Geen profiel'), (b'Co', b'Consument'), (b'Ve', b'Verzamelaar'), (b'St', b'Strateeg'), (b'Ne', b'Netwerker'), (b'On', b'Ontwerper')]),
            preserve_default=True,
        ),
    ]
