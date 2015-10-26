# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0022_auto_20150507_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='provincie',
            field=models.CharField(max_length=b'2', choices=[(None, b'Geen provincie'), (b'GR', b'Groningen'), (b'FR', b'Friesland'), (b'DR', b'Drenthe'), (b'OV', b'Overijssel'), (b'FL', b'Flevoland'), (b'GE', b'Gelderland'), (b'UT', b'Utrecht'), (b'NO', b'Noord-Holland'), (b'ZU', b'Zuid-Holland'), (b'ZE', b'Zeeland'), (b'NB', b'Noord-Brabant'), (b'LI', b'Limburg'), (b'BE', b'Belgie'), (b'DU', b'Duitsland'), (b'FA', b'Frankrijk'), (b'VE', b'Verenigd Koningkrijk'), (b'LU', b'Luxemburg'), (b'AN', b'Andere')]),
            preserve_default=True,
        ),
    ]
