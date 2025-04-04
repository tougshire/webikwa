# Generated by Django 5.1.7 on 2025-03-27 15:22

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('webikwa', '0004_alter_articlepageimage_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlestatictagsindexpage',
            name='full_body_groups',
            field=models.CharField(default='1', help_text="A comma separated list of the tag group numbers for which the full body instead of summary should be shown in an index page. '1' is the first group.  ex: '1,2'", max_length=30, verbose_name='Full Body Groups'),
        ),
        migrations.RemoveField(
            model_name='articlestatictagsindexpage',
            name='show_body_in_index',
        ),

    ]
