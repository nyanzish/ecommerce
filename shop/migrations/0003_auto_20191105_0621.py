# Generated by Django 2.2 on 2019-11-05 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20191105_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Cows', 'Cows'), ('Chicken', 'Chicken'), ('Goats', 'Goats')], max_length=10),
        ),
    ]
