# Generated by Django 2.1.7 on 2019-03-05 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_statements_reader', '0003_auto_20190304_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='flow_type',
        ),
        migrations.AddField(
            model_name='transaction',
            name='statement_number',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
    ]