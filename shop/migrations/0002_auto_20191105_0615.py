# Generated by Django 2.2 on 2019-11-05 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Cows', 'Cows'), ('Chicken', 'Chicken'), ('Goats', 'Goats')], max_length=2),
        ),
    ]