# Generated by Django 2.2.17 on 2020-12-31 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wtsapp', '0002_auto_20201230_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='working',
            name='approve_time',
            field=models.DateTimeField(blank=True, default=None, help_text='审批通过时间'),
        ),
    ]