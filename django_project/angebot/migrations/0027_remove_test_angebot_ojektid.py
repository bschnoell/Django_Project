# Generated by Django 3.0.8 on 2020-12-11 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('angebot', '0026_auto_20201210_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test_angebot',
            name='ojektid',
        ),
    ]
