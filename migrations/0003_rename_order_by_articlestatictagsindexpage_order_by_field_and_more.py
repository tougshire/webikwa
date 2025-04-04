# Generated by Django 5.1.7 on 2025-03-26 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webikwa', '0002_articlesingularpage_delete_freearticlepage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlestatictagsindexpage',
            old_name='order_by',
            new_name='order_by_field',
        ),
        migrations.RenameField(
            model_name='sidebarpage',
            old_name='order_by',
            new_name='order_by_field',
        ),
        migrations.RemoveField(
            model_name='articleindexpage',
            name='order_by',
        ),
        migrations.AddField(
            model_name='articleindexpage',
            name='order_by_field',
            field=models.CharField(blank=True, choices=[('-order_by_date', 'Orderby Date >'), ('order_by_date', 'Orderby Date <'), ('-latest_revision_created_at', 'Update Date/Time >'), ('latest_revision_created_at', 'Update Date/Time <'), ('-first_published_at', 'Publish Date/Time >'), ('first_published_at', 'Publish Date/Time <'), ('title', 'Title'), ('-title', 'Title >')], default='-order_by_date', help_text='The article attribute to determine the order in which articles will be displayed', max_length=40),
        ),
    ]
