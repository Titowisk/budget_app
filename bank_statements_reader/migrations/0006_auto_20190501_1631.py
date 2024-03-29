# Generated by Django 2.1.7 on 2019-05-01 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank_statements_reader', '0005_auto_20190501_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='month',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='months', to='bank_statements_reader.Year'),
        ),
        migrations.AddField(
            model_name='year',
            name='name',
            field=models.CharField(default=2019, max_length=4),
        ),
    ]
