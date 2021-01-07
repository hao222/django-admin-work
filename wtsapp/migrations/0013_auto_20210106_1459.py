# Generated by Django 2.2.17 on 2021-01-06 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wtsapp', '0012_auto_20210106_1056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='working',
            name='fail_reasons',
        ),
        migrations.AddField(
            model_name='working',
            name='reasons',
            field=models.CharField(blank=True, default='', help_text='建议', max_length=32, null=True),
        ),
    ]