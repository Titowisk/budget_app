# Generated by Django 2.1.7 on 2019-03-04 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank_statements_reader', '0002_auto_20190303_2025'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transactions',
            new_name='Transaction',
        ),
    ]
