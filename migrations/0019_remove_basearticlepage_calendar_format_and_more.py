# Generated by Django 5.2.4 on 2025-07-04 03:14

import django.db.models.deletion
import modelcluster.fields
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0094_alter_page_locale'),
        ('webikwa', '0018_alter_icalendarlinkpage_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basearticlepage',
            name='calendar_format',
        ),
        migrations.RemoveField(
            model_name='basearticlepage',
            name='ical_start_span_count',
        ),
        migrations.RemoveField(
            model_name='basearticlepage',
            name='calendar_dt_format',
        ),
        migrations.RemoveField(
            model_name='basearticlepage',
            name='calendars',
        ),
        migrations.CreateModel(
            name='IcalendarIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True)),
                ('show_pagetitle', models.BooleanField(default=True, help_text='If the page title should be shown')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='icalendarpage',
            name='delete_stale_links_blocks',
            field=models.BooleanField(default=True, help_text='Upon save, automaticall delete links and blocks for events that are no longer on this calendar', verbose_name='delete stale links & blocks'),
        ),
        migrations.CreateModel(
            name='IcalCombinerPage',
            fields=[
                ('basearticlepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='webikwa.basearticlepage')),
                ('ical_start_span_count', models.CharField(blank=True, default='-1,3660', help_text='Comma separated numbers representing the number of days to the starting date (can be negative), the number of days from the starting date to the ending date, and the max number of events to return', max_length=20, verbose_name='start,span,count')),
                ('calendar_format', models.CharField(choices=[('EVLS', 'event list'), ('DTLS', 'date list')], default='EVLS', help_text='The format for how the events are displayed', max_length=4, verbose_name='calendar format')),
                ('calendar_dt_format', models.CharField(default='D Y M d|g:iA', help_text='The date and time formats separated by a bar ex: D Y M d|g:iA', max_length=40, verbose_name='calendar date and time formats')),
                ('calendars', modelcluster.fields.ParentalManyToManyField(blank=True, to='webikwa.icalendarpage')),
            ],
            options={
                'verbose_name': 'iCalendar Combiner',
            },
            bases=('webikwa.basearticlepage',),
        ),
    ]
