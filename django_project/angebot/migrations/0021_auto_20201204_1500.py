# Generated by Django 3.0.8 on 2020-12-04 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angebot', '0020_test_angebot_kundenid'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_angebot',
            name='anschlussS',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='test_angebot',
            name='gesamtsumme',
            field=models.IntegerField(default='0'),
        ),
    ]
