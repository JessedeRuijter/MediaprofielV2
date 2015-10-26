# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('progress', models.IntegerField(default=0)),
                ('answers', models.CommaSeparatedIntegerField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChoiceScores',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consument', models.IntegerField(default=0)),
                ('verzamelaar', models.IntegerField(default=0)),
                ('strateeg', models.IntegerField(default=0)),
                ('netwerker', models.IntegerField(default=0)),
                ('producent', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Enquete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('publishedDate', models.DateTimeField(verbose_name=b'date published')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('leeftijd', models.IntegerField()),
                ('opleiding', models.CharField(max_length=b'2', choices=[(None, b'Geen opleiding'), (b'M', b'MBO'), (b'H', b'HBO'), (b'W', b'WO')])),
                ('provincie', models.CharField(max_length=b'2', choices=[(None, b'Geen provincie'), (b'GR', b'Groningen'), (b'FR', b'Friesland'), (b'DR', b'Drenthe'), (b'OV', b'Overijssel'), (b'FL', b'Flevoland'), (b'GE', b'Gelderland'), (b'UT', b'Utrecht'), (b'NO', b'Noord-Holland'), (b'ZU', b'Zuid-Holland'), (b'ZE', b'Zeeland'), (b'NB', b'Noord-Brabant')])),
                ('actief', models.CharField(max_length=b'5')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('members', models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL)),
                ('owners', models.ManyToManyField(related_name='owners', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profiel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consument', models.IntegerField(default=0)),
                ('verzamelaar', models.IntegerField(default=0)),
                ('strateeg', models.IntegerField(default=0)),
                ('netwerker', models.IntegerField(default=0)),
                ('producent', models.IntegerField(default=0)),
                ('completedBlocks', models.CommaSeparatedIntegerField(default=b'', max_length=1000)),
                ('user', models.ForeignKey(related_name='profiel', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('questionText', models.TextField()),
                ('order', models.IntegerField(default=0)),
                ('qType', models.CharField(max_length=1, choices=[(b'Y', b'YesNo'), (b'M', b'MultipeChoice'), (b'S', b'Slider')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('enquete', models.ForeignKey(related_name='blocks', to='vragenlijsten.Enquete')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choiceText', models.CharField(max_length=200)),
                ('question', models.ForeignKey(related_name='choices', to='vragenlijsten.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='block',
            field=models.ForeignKey(related_name='questions', to='vragenlijsten.QuestionBlock'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='choicescores',
            name='choice',
            field=models.ForeignKey(related_name='score', to='vragenlijsten.QuestionChoice'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='blockID',
            field=models.ForeignKey(to='vragenlijsten.QuestionBlock'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
