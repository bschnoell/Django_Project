# Generated by Django 3.0.8 on 2020-12-14 12:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('angebot', '0032_auto_20201214_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test_Angebot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(blank=True, default='', max_length=100)),
                ('gesamtsumme', models.IntegerField(blank=True, default='0', null=True)),
                ('anschlussS', models.IntegerField(blank=True, default='0', null=True)),
                ('anschlussM', models.IntegerField(blank=True, default='0', null=True)),
                ('anschlussL', models.IntegerField(blank=True, default='0', null=True)),
                ('datum_erstellt', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.BooleanField(choices=[(True, 'offen'), (False, 'abgeschlossen')], default=True)),
                ('kundenid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='angebot.Test_Kunde')),
            ],
        ),
        migrations.CreateModel(
            name='Test_Baustoff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('art', models.CharField(max_length=100)),
                ('wert', models.IntegerField(default='0')),
            ],
        ),
        migrations.CreateModel(
            name='Test_Bauweise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('art', models.CharField(max_length=100)),
                ('bezeichnung', models.CharField(blank=True, default='', max_length=100)),
                ('energiekennzahl', models.CharField(blank=True, default='', max_length=50)),
                ('wert', models.IntegerField(default='0')),
            ],
        ),
        migrations.CreateModel(
            name='Test_Heizkoerper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bezeichnung', models.CharField(blank=True, default='', max_length=100)),
                ('preis', models.IntegerField(default='0')),
            ],
        ),
        migrations.CreateModel(
            name='Test_Objekt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bezeichnung', models.CharField(blank=True, default='', max_length=100)),
                ('dickeaussenwand', models.IntegerField(blank=True, default='0', null=True)),
                ('dickedaemmung', models.IntegerField(default='0')),
                ('uwert', models.IntegerField(default='0')),
                ('fensterqualitaet', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('angebotid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angebot.Test_Angebot')),
                ('baustoffid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angebot.Test_Baustoff')),
                ('bauweiseid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angebot.Test_Bauweise')),
            ],
        ),
        migrations.CreateModel(
            name='Test_Steuerung',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('preis', models.IntegerField(default='0')),
            ],
        ),
        migrations.CreateModel(
            name='Test_Raum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('hoehe', models.IntegerField(default='0')),
                ('flaeche', models.IntegerField(default='0')),
                ('anzfenster', models.IntegerField(default='0')),
                ('anzaussenfenster', models.IntegerField(default='0')),
                ('alternative', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('s', models.IntegerField(default='0')),
                ('m', models.IntegerField(default='0')),
                ('l', models.IntegerField(default='0')),
                ('es980', models.IntegerField(default='0')),
                ('es981', models.IntegerField(default='0')),
                ('es982', models.IntegerField(default='0')),
                ('es800', models.IntegerField(default='0')),
                ('es810', models.IntegerField(default='0')),
                ('es820', models.IntegerField(default='0')),
                ('es700', models.IntegerField(default='0')),
                ('objektid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angebot.Test_Objekt')),
            ],
        ),
    ]
