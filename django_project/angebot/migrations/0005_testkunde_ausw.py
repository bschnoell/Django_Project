# Generated by Django 3.0.8 on 2020-11-19 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angebot', '0004_auto_20201119_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='testkunde',
            name='ausw',
            field=models.CharField(choices=[('Ausw1', 'Ausw2'), ('Ausw2', 'ausw2')], default='Ausw1', max_length=10),
        ),
    ]
