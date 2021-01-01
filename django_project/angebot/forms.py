from django import forms
from .models import * #alle Tabellen importieren


#TODO: Pflichtfelder definieren (zB Bei Raum müssen einige Felder befüllt sein, sonst kann nicht berechnet werden)
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
        fields = ['name', 'hoehe', 'flaeche', 'anzfenster', 'anzaussenflaechen', 'alternative']
        labels = {'name': 'Raum-Name'}


class ObjektForm(forms.ModelForm):

    #Zusätzliches Choice Feld zu forms.modelform hinzufügen
    #Erster Eintrag = --Auswählen--
    Baustoff_choices = [('0', '--Auswählen--')]
    for i in Test_Baustoff.objects.all():
        Baustoff_choices.append(
            (i.id, i.art)
            #hier wird in der datenbank der lambdawert angezeigt, der kann für die berechnung dann direkt
            #verwendet werden. im Form choices Feld
           # (i.lambdawert, i.art)
        )  # second element is what is this what will be displayed in template

    #hinzufügen eines zusätzlichen feldes das eigentlich nicht in der datenbank ist
    baustoff = forms.ChoiceField(choices=Baustoff_choices)

    class Meta:
        model = Test_Objekt
        fields = ['bezeichnung', 'baustoff', 'dickeaussenwand', 'dickedaemmung', 'fensterqualitaet']
        labels = {'bezeichnung': 'Objekt-Bez'}


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


