# Generated by Django 5.0.3 on 2024-04-30 18:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_expense_financialsummary_incomesource_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='incomesource',
            name='date',
            field=models.DateField(default='2024-04-30'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expense',
            name='frequency',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='incomesource',
            name='frequency',
            field=models.CharField(max_length=100),
        ),
    ]