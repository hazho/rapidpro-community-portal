# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.fields
import modelcluster.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0005_make_filter_spec_unique'),
        ('wagtailcore', '0013_update_golive_expire_help_text'),
        ('portal_pages', '0004_casestudyindexpage_casestudypage_countrycasestudy_focusareacasestudy_organizationcasestudy_techfirmc'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseStudyHeroImageItem',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(blank=True, null=True, editable=False)),
                ('blurb', wagtail.core.fields.RichTextField()),
                ('casestudy_page', modelcluster.fields.ParentalKey(to='portal_pages.CaseStudyPage', related_name='case_study_hero_items')),
                ('hero_image', models.ForeignKey(to='wagtailimages.Image', on_delete=django.db.models.deletion.CASCADE)),
                ('target_page', models.ForeignKey(to='wagtailcore.Page', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
    ]
