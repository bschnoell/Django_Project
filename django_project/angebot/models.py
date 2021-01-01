from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms

#TODO: Erstellt Datum hinzufügen
#TODO: Status bei Angebot
#TODO: Rabatt bei Angebot

class Test_Kunde(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    kunde = models.CharField(max_length=250,default='', blank=True)
    plz = models.CharField(max_length=4, default='', blank=True)
    ort = models.CharField(max_length=30, default='', blank=True)
    telefonnr = models.CharField(max_length=15, default='', blank=True)
    mail = models.EmailField(max_length=100, default='', blank=True)
    strasse = models.CharField(max_length=100, default='', blank=True)
    heiztage = models.IntegerField(default=0)
    raumtemp = models.IntegerField(default=0)
    stromkosten = models.CharField(max_length=50, default='', blank=True)

class Test_Bauweise(models.Model):
    art = models.CharField(max_length=100)
    bezeichnung = models.CharField(max_length=100, default='', blank=True)
    energiekennzahl = models.CharField(max_length=50, default='', blank=True)
    wert = models.IntegerField(default='0')


class Test_Baustoff(models.Model):
    art = models.CharField(max_length=100)
    wert = models.IntegerField(default='0')
    lambdawert  = models.FloatField(default=0)

class t_config(models.Model):
    art = models.CharField(max_length=100)
    wert = models.FloatField(default='0')

class t_lambda(models.Model):
    art = models.CharField(max_length=100)
    wert = models.FloatField(default='0')

class Test_Angebot(models.Model):
    BOOL_CHOICES = ((True, 'offen'), (False, 'abgeschlossen'))

    kundenid = models.ForeignKey(Test_Kunde, on_delete=models.CASCADE, blank=True, null=True)
    titel = models.CharField(max_length=100, default='', blank=True)
    gesamtsumme = models.IntegerField(default='0', blank=True, null=True)
    anschlussS = models.IntegerField(default='0', blank=True, null=True)
    anschlussM = models.IntegerField(default='0', blank=True, null=True)
    anschlussL = models.IntegerField(default='0', blank=True, null=True)
    datum_erstellt = models.DateTimeField(default=timezone.now) #timezone.now ist eine funktion, aber hier keine () am Ende, hier wird nur der name der funktion übergeben
    status = models.BooleanField(choices=BOOL_CHOICES, default=True)

    def get_absolute_url(self):
        return reverse('angebot_details', kwargs={'pk': self.pk})



class Test_Objekt(models.Model):

    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

    angebotid = models.ForeignKey(Test_Angebot, on_delete=models.CASCADE)
    #baustoffid = models.ForeignKey(Test_Baustoff, on_delete=models.CASCADE)#alt
    #baustoffid = models.IntegerField(default=0)#alt
    #TODO: bauweiseid noch umschreiben - wie baustoff id choose feld machen
    #bauweiseid = models.ForeignKey(Test_Bauweise, on_delete=models.CASCADE)

    #baustofffeld wird über das choices feld in models gespeichert
    baustoff = models.IntegerField(default=0)
    bezeichnung = models.CharField(max_length=100, default='', blank=True)
    dickeaussenwand = models.IntegerField(default='0', blank=True, null=True)
    dickedaemmung = models.IntegerField(default='0')
    uwert = models.IntegerField(default='0')
    fensterqualitaet = models.BooleanField(choices=BOOL_CHOICES, default=True)

class Test_Raum(models.Model):

    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    objektid = models.ForeignKey(Test_Objekt, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='', blank=True)
    hoehe = models.IntegerField(default='0')
    flaeche = models.IntegerField(default='0')
    anzfenster = models.IntegerField(default='0')
    # das Feld gehört noch gelöscht!!!
    anzaussenfenster = models.IntegerField(default='0')#das Feld gehört noch gelöscht!!!
    anzaussenflaechen = models.IntegerField(default='0')
    alternative = models.BooleanField(choices=BOOL_CHOICES, default=False)
    anzS = models.IntegerField(default='0')
    anzM = models.IntegerField(default='0')
    anzL = models.IntegerField(default='0')
    es980 = models.IntegerField(default='0')
    es981 = models.IntegerField(default='0')
    es982 = models.IntegerField(default='0')
    es800 = models.IntegerField(default='0')
    es810 = models.IntegerField(default='0')
    es820 = models.IntegerField(default='0')
    es700 = models.IntegerField(default='0')

class Test_Heizkoerper(models.Model):
    bezeichnung = models.CharField(max_length=100, default='', blank=True)
    preis = models.IntegerField(default='0')

class Test_Steuerung(models.Model):
    name = models.CharField(max_length=100, default='', blank=True)
    preis = models.IntegerField(default='0')

#class MyModelForm(forms.ModelForm):
#    class Meta:
#        model = MyModel
#        widgets = {
#            'alternative': forms.RadioSelect
#        }

#Hier wird Tabelle Post erstellt
class Testkunde(models.Model):
    auswahl = (
        ('Ausw1', 'Ausw2'),
        ('Ausw2', 'ausw2'),
        ('Ausw3', 'ausw3'),
    )

    vname = models.CharField(max_length=250,default='vname')
    nname = models.TextField(default='default')
    tel = models.CharField(max_length=250,default='0664')
    ausw = models.CharField(max_length=10,choices=auswahl,default="Ausw1")
    datum = models.DateTimeField(default=timezone.now)
    zahl1 = models.IntegerField(default=1)
    zahl2 = models.IntegerField(default=2)
    result = models.IntegerField(default=0)

    def __str__(self):
        return self.vname

   # def get_absolute_url(self):
  #     return reverse('angebot:testkunde_list',)

    def get_result(self):
        erg = self.zahl1 + self.zahl2
        return erg

    def save(self, *args, **kwargs):
        self.result = self.get_result()
        super(Testkunde, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('angebot-detail', kwargs={'pk': self.pk})

class Testangebot(models.Model):
    kunde = models.ForeignKey(Testkunde, on_delete=models.CASCADE)
    angebotname = models.CharField(max_length=50,default='Angebot:')
    wert1 = models.IntegerField(default=5)
    wert2 = models.IntegerField(default=7)

    def __str__(self):
        return self.angebotname
