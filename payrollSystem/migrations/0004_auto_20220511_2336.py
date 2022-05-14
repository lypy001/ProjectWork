# Generated by Django 3.2.13 on 2022-05-11 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payrollSystem', '0003_attendance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='personschedule',
            options={'ordering': ['-date']},
        ),
        migrations.RemoveField(
            model_name='personschedule',
            name='date_end',
        ),
        migrations.RemoveField(
            model_name='personschedule',
            name='date_start',
        ),
        migrations.AddField(
            model_name='personschedule',
            name='date',
            field=models.DateField(null=True),
        ),
    ]