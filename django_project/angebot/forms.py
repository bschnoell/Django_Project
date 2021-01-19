from django import forms
from .models import * #alle Tabellen importieren


#TODO: Pflichtfelder definieren (zB Bei Raum müssen einige Felder befüllt sein, sonst kann nicht berechnet werden)
class KundeForm(forms.ModelForm):

    class Meta:
        model = Test_Kunde
        fields = ['kunde', 'plz', 'ort', 'strasse', 'telefonnr', 'mail', 'heiztage', 'raumtemp', 'stromkosten' ]
        labels = {'kunde': 'Kunde:', 'plz': 'Plz.:', 'ort': 'Ort:',
                  'strasse': 'Straße:', 'telefonnr': 'Tel.Nr.:',
                  'mail': 'E-Mail:', 'heiztage': 'Heiztage:',
                  'raumtemp': 'Raumtemperatur:','stromkosten': 'Stromkosten:',}


class AngebotForm(forms.ModelForm):

    class Meta:
        model = Test_Angebot
        fields = ['titel']
        labels = {'titel': 'Angebot-Titel'}


class RaumForm(forms.ModelForm):

    class Meta:
        model = Test_Raum
        fields = ['name', 'hoehe', 'flaeche', 'anzfenster', 'anzaussenflaechen', 'alternative', 'anzS', 'anzM', 'anzL', 'anzManuellUeberschrieben']
        labels = {'name': 'Name:', 'hoehe': 'Höhe:', 'flaeche': 'Fläche:',
                  'anzfenster': '#Fenster:', 'anzaussenflaechen': '#Außenflächen:',
                  'alternative': 'Alternative:', 'anzS': 'Anzahl Heizkörper Small',
                  'anzM': 'Anzahl Heizkörper Medium', 'anzL': 'Anzahl Heizkörper Large',
                  'anzManuellUeberschrieben': '# manuell überschreiben'
                  }
class HeizkostenabschaetzungraumForm(forms.ModelForm):

    class Meta:
        model = T_Heizkostenabschaetzung_Raum
        fields = []

class ObjektForm(forms.ModelForm):

    #Zusätzliches Choice Feld zu forms.modelform hinzufügen
    #Erster Eintrag = --Auswählen--
 #   Baustoff_choices = [('0', '--Auswählen--')]
    Baustoff_choices= []
    for i in Test_Baustoff.objects.all():
        Baustoff_choices.append(
            (i.id, i.art)
            #hier wird in der datenbank der lambdawert angezeigt, der kann für die berechnung dann direkt
            #verwendet werden. im Form choices Feld
           # (i.lambdawert, i.art)
        )  # second element is what is this what will be displayed in template

  #  Bauweiseid_choices = [('0', '--Auswählen--')]
    Bauweiseid_choices = []
    for y in T_Bauweise.objects.all():
        Bauweiseid_choices.append(
            (y.id, y.art)
        )


    #hinzufügen eines zusätzlichen feldes das eigentlich nicht in der datenbank ist
    baustoff = forms.ChoiceField(choices=Baustoff_choices)
    bauweiseid = forms.ChoiceField(choices=Bauweiseid_choices)

    class Meta:
        model = Test_Objekt
        fields = ['bezeichnung', 'baustoff', 'bauweiseid', 'dickeaussenwand', 'dickedaemmung', 'fensterqualitaet']
        labels = {'bezeichnung': 'Bezeichnung:', 'baustoff': 'Baustoff:',
                  'bauweiseid': 'Bauweise:', 'dickeaussenwand': 'Stärke Außenwand in cm',
                  'dickedaemmung': 'Stärke Dämmung in cm', 'fensterqualitaet': 'Fensterqualität'}


    def save(self, commit=True):
        # Ist glaub ich nötig damit das hier hinzugefügte Choice Feld angezeigt wird.
     #   q_baustoff = Test_Baustoff.objects.get(pk=self.cleaned_data['baustoff'])
       # baustoff = q_baustoff.art
        return super(ObjektForm, self).save(commit=commit)


'''
class BaustoffForm(forms.ModelForm):

    class Meta:
        model = Test_Baustoff
        fields = ['art']

class BauweiseForm(forms.ModelForm):

    class Meta:
        model = Test_Bauweise
        fields = ['art']


'''





###########
#alt
##############
class KundeCreationForm(forms.ModelForm):

    class Meta:
        model = Test_Kunde
        fields = ['kunde']


