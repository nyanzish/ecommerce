# Generated by Django 2.2.6 on 2019-11-26 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_auto_20191126_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem2',
            name='saler',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Farmer'),
        ),
    ]
