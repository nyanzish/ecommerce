# Generated by Django 2.2.6 on 2019-11-26 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_auto_20191126_2250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem2',
            old_name='saler',
            new_name='saler1',
        ),
        migrations.RemoveField(
            model_name='farmer',
            name='user',
        ),
    ]
