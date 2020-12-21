from django import forms
from .models import * #alle Tabellen importieren

class KundeForm(forms.ModelForm):

    class Meta:
        model = Test_Kunde
        fields = ['kunde']

class AngebotForm(forms.ModelForm):

    class Meta:
        model = Test_Angebot
        fields = ['titel']
        labels = {'titel': 'Angebot-Titel'}

class RaumForm(forms.ModelForm):

    class Meta:
        model = Test_Raum
        fields = ['name', 'hoehe', 'flaeche', 'anzfenster', 'anzaussenfenster']
        labels = {'name': 'Raum-Name'}

class ObjektForm(forms.ModelForm):

    class Meta:
        model = Test_Objekt
 #       fields = ['bezeichnung']
        fields = ['bezeichnung', 'baustoffid', 'bauweiseid']
        labels = {'bezeichnung': 'Objekt-Bez'}


class BaustoffForm(forms.ModelForm):

    class Meta:
        model = Test_Baustoff
        fields = ['art']

class BauweiseForm(forms.ModelForm):

    class Meta:
        model = Test_Bauweise
        fields = ['art']








###########
#alt
##############
class KundeCreationForm(forms.ModelForm):

    class Meta:
        model = Test_Kunde
        fields = ['kunde']


