# Generated by Django 3.0.7 on 2020-07-20 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200717_0555'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follow_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='follower_count',
            field=models.IntegerField(default=0),
        ),
    ]
