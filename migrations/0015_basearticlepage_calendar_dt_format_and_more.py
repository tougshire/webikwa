# Generated by Django 5.1.7 on 2025-06-04 17:00

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webikwa', '0014_alter_icalendarlinkpage_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='basearticlepage',
            name='calendar_dt_format',
            field=models.CharField(default='D Y M d|g:iA', help_text='The date and time formats separated by a bar ex: D Y M d|g:iA', max_length=40, verbose_name='calendar date and time formats'),
        ),
        migrations.AddField(
            model_name='icalendarlinkpage',
            name='article',
            field=modelcluster.fields.ParentalKey(blank=True, help_text='An article to link to.  Ensure the url field is blank to use this field', null=True, on_delete=django.db.models.deletion.SET_NULL, to='webikwa.articlepage'),
        ),
        migrations.AlterField(
            model_name='basearticlepage',
            name='calendar_format',
            field=models.CharField(choices=[('EVLS', 'event list'), ('DTLS', 'date list')], default='EVLS', help_text='The format for how the events are displayed', max_length=4, verbose_name='calendar format'),
        ),
        migrations.AlterField(
            model_name='icalendarlinkpage',
            name='uid',
            field=models.CharField(help_text='The UID of the event from ics data', max_length=120),
        ),
        migrations.AlterField(
            model_name='icalendarlinkpage',
            name='url',
            field=models.URLField(blank=True, help_text='The URL to link to. Leave blank if linking to an article using the Article field'),
        ),
    ]
