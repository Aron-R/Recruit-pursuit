# Generated by Django 3.1.2 on 2021-06-08 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0012_job_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='tags',
        ),
    ]
