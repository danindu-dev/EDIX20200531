# Generated by Django 3.0.5 on 2020-06-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BPMS', '0005_auto_20200614_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mc_details',
            name='mc_contact_person_mob',
            field=models.CharField(max_length=225),
        ),
        migrations.AlterField(
            model_name='mc_details',
            name='mc_main_tele',
            field=models.CharField(max_length=225),
        ),
    ]
