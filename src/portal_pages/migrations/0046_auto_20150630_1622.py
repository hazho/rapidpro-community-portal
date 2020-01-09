# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_pages', '0045_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='highlightitem',
            name='target_page_external',
            field=models.CharField(verbose_name='External target page (leave blank if Target page is selected.)', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='homepageheroimageitem',
            name='blurb',
            field=models.CharField(max_length=255),
        ),
    ]
