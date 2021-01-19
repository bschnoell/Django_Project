from django import template
from django.apps.config import AppConfig
from angebot.models import Test_Angebot

register = template.Library()

#Benutzerdefinierte Funktion, um im Template zu filtern
@register.simple_tag() #muss je nachdem welche Art von Funktion es hat mit .simple_tag() oder .filter() etc registriert werden
def get_angebote_filter_status_offen(kunde):
    #übergabe von kunden und returned alle Angebote des Kunden mit Status offen
    #TODO: Orderby funktioniert nicht ??
    angebote = kunde.test_angebot_set.filter(status="offen").order_by('-datum_erstellt')
    return angebote

@register.simple_tag()
def get_angebote_filter_status_verkauft(kunde):
    #übergabe von kunden und returned alle Angebote des Kunden mit Status offen
    angebote = kunde.test_angebot_set.filter(status="verkauft")
    return angebote

@register.simple_tag()
def get_angebote_filter_status_nicht_verkauft(kunde):
    #übergabe von kunden und returned alle Angebote des Kunden mit Status offen
    angebote = kunde.test_angebot_set.filter(status="nicht verkauft")
    return angebote


