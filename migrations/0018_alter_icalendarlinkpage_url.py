# Generated by Django 5.1.7 on 2025-06-18 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webikwa', '0017_icalendarblockpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icalendarlinkpage',
            name='url',
            field=models.CharField(blank=True, help_text='The URL to link to. Leave blank if linking to an article using the Article field', max_length=200),
        ),
    ]
