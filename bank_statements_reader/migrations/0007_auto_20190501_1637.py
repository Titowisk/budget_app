# Generated by Django 2.1.7 on 2019-05-01 19:37

import bank_statements_reader.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_statements_reader', '0006_auto_20190501_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='name',
            field=models.CharField(default=bank_statements_reader.models.Year.name_default, max_length=4),
        ),
    ]