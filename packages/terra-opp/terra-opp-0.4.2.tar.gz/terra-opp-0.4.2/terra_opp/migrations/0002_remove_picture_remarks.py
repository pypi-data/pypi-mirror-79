# Generated by Django 2.2.5 on 2019-10-09 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terra_opp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='remarks',
        ),
    ]
