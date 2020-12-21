# Generated by Django 3.0.8 on 2020-11-29 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('angebot', '0008_testkunde_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testangebot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('angebotname', models.CharField(default='Angebot:', max_length=50)),
                ('wert1', models.IntegerField(default=5)),
                ('wert2', models.IntegerField(default=7)),
                ('kunde', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angebot.Testkunde')),
            ],
        ),
    ]
