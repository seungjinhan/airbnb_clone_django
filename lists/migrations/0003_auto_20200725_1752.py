# Generated by Django 2.2.5 on 2020-07-25 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_auto_20200725_0008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='room',
            new_name='rooms',
        ),
    ]
