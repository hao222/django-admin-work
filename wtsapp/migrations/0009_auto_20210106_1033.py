# Generated by Django 2.2.17 on 2021-01-06 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wtsapp', '0008_taskpro_task_process'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskpro',
            name='task_process',
            field=models.CharField(default='0', help_text='任务进度，0-100', max_length=2, verbose_name='任务进度'),
        ),
    ]
