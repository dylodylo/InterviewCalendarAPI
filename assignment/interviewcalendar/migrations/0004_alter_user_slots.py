# Generated by Django 3.2.3 on 2021-05-27 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviewcalendar', '0003_alter_user_slots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slots',
            field=models.JSONField(default=dict),
        ),
    ]
