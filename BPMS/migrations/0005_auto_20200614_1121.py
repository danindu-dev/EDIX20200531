# Generated by Django 3.0.5 on 2020-06-14 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BPMS', '0004_mc_details_mc_lastinvoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub_bank',
            name='status',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sub_clients',
            name='status',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
