# Generated by Django 3.0.8 on 2020-11-27 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angebot', '0007_auto_20201127_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='testkunde',
            name='result',
            field=models.IntegerField(default=0),
        ),
    ]
