# Generated by Django 3.0.8 on 2020-12-11 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('angebot', '0029_auto_20201211_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test_angebot',
            name='anschlussL',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='test_angebot',
            name='anschlussM',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='test_angebot',
            name='anschlussS',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='test_angebot',
            name='gesamtsumme',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='test_angebot',
            name='kundenid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='angebot.Test_Kunde'),
        ),
        migrations.AlterField(
            model_name='test_angebot',
            name='titel',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='test_baustoff',
            name='baustoffart',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='test_bauweise',
            name='bauweiseart',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='test_bauweise',
            name='bauweisebezeichnung',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='test_heizkoerper',
            name='bezeichnung',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='test_kunde',
            name='kunde',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='test_kunde',
            name='mail',
            field=models.EmailField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='test_kunde',
            name='ort',
            field=models.CharField(blank=True, default='', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='test_kunde',
            name='plz',
            field=models.CharField(blank=True, default='', max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='test_kunde',
            name='strasse',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='test_kunde',
            name='stromkosten',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='test_kunde',
            name='telefonnr',
            field=models.CharField(blank=True, default='', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='test_kunde',
            name='userid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='test_objekt',
            name='angebotid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='angebot.Test_Angebot'),
        ),
        migrations.AlterField(
            model_name='test_objekt',
            name='baustoffid',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='angebot.Test_Baustoff'),
        ),
        migrations.AlterField(
            model_name='test_objekt',
            name='bauweiseid',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='angebot.Test_Bauweise'),
        ),
        migrations.AlterField(
            model_name='test_objekt',
            name='bezeichnung',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='test_objekt',
            name='dickeaussenwand',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='test_raum',
            name='name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='test_raum',
            name='objektid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='angebot.Test_Objekt'),
        ),
        migrations.AlterField(
            model_name='test_steuerung',
            name='name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]