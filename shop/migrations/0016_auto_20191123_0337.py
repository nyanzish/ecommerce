# Generated by Django 2.2.6 on 2019-11-23 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='shiping_address',
            new_name='shipping_address',
        ),
        migrations.AddField(
            model_name='address',
            name='shipping_city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]