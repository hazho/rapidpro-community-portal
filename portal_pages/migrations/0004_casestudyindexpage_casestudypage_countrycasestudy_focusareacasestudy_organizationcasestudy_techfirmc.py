# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0013_update_golive_expire_help_text'),
        ('wagtailimages', '0005_make_filter_spec_unique'),
        ('portal_pages', '0003_focusarea_organization_techfirm'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseStudyIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, parent_link=True, serialize=False, auto_created=True, to='wagtailcore.Page', on_delete=django.db.models.deletion.CASCADE)),
                ('intro', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='CaseStudyPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, parent_link=True, serialize=False, auto_created=True, to='wagtailcore.Page', on_delete=django.db.models.deletion.CASCADE)),
                ('summary', wagtail.core.fields.RichTextField()),
                ('date', models.DateField(verbose_name='Post date')),
                ('feed_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', blank=True, to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='CountryCaseStudy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, null=True, editable=False)),
                ('country', models.ForeignKey(related_name='+', to='portal_pages.Country', on_delete=django.db.models.deletion.CASCADE)),
                ('page', modelcluster.fields.ParentalKey(related_name='countries', to='portal_pages.CaseStudyPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FocusAreaCaseStudy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, null=True, editable=False)),
                ('focusarea', models.ForeignKey(related_name='+', to='portal_pages.FocusArea', on_delete=django.db.models.deletion.CASCADE)),
                ('page', modelcluster.fields.ParentalKey(related_name='focus_areas', to='portal_pages.CaseStudyPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationCaseStudy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, null=True, editable=False)),
                ('organization', models.ForeignKey(related_name='+', to='portal_pages.Organization', on_delete=django.db.models.deletion.CASCADE)),
                ('page', modelcluster.fields.ParentalKey(related_name='organizations', to='portal_pages.CaseStudyPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TechFirmCaseStudy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, null=True, editable=False)),
                ('page', modelcluster.fields.ParentalKey(related_name='tech_firms', to='portal_pages.CaseStudyPage')),
                ('techfirm', models.ForeignKey(related_name='+', to='portal_pages.TechFirm', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
    ]
