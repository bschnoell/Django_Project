# Generated by Django 3.0.8 on 2020-12-14 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angebot', '0032_auto_20201214_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test_bauweise',
            name='id',
        ),
        migrations.AlterField(
            model_name='test_bauweise',
            name='art',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]