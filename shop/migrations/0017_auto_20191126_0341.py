# Generated by Django 2.2.6 on 2019-11-26 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20191123_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='saler',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Farmer'),
        ),
        migrations.AlterField(
            model_name='address',
            name='shipping_city',
            field=models.CharField(max_length=100),
        ),
    ]
