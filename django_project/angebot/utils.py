#Py Fil für Hilfsprogramme


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from .models import *
from xhtml2pdf import pisa

#Source von https://www.codingforentrepreneurs.com/blog/html-template-to-pdf-in-django übernommen
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


#Berechnung des ERS Algorithmus
def get_anz_heizkoerper( l_raum, l_objekt):

    # Eingabewerte
    raumhoehe = l_raum.hoehe  # in meter
    raumflaeche = l_raum.flaeche  # in qm
    anzfenster = l_raum.anzfenster
    anzaussenwaende = l_raum.anzaussenflaechen
    staerkedaemmung = l_objekt.dickedaemmung  # in cm
    #Stärke Dämmung wird auf 12 maximal "gedeckelt"
    if staerkedaemmung > 12:
        staerkedaemmung = 12

    staerkeaussenwand = l_objekt.dickeaussenwand  # in cm

    # Fixwerte
    #mit get bekommt man immer nur einen eintrag
    q_aufschlagfenster = t_config.objects.get(art='aufschlagfenster')
    q_aufschlagwaende = t_config.objects.get(art='aufschlagwaende')
    q_aufschlagueberdimensionierung = t_config.objects.get(art='aufschlagueberdimensionierung')
    q_abschlagdaemmung = t_config.objects.get(art='abschlagdaemmung')


    aufschlagfenster = q_aufschlagfenster.wert  # 5%
    aufschlagwaende = q_aufschlagwaende.wert  # 5%
    aufschlagueberdimensionierung = q_aufschlagueberdimensionierung.wert  # 10%

    abschlagdaemmung = q_abschlagdaemmung.wert  # 2%

    # uwert Berechnung - je nach Bauweise:

    #ID/PK von Baustoff wird direkt in Objekt tabelle gespeichert, funktioniert über choices feld
    #in model.forms von objekt...
    q_baustoff = Test_Baustoff.objects.get(id=l_objekt.baustoff)

    lambdabaustoff = q_baustoff.lambdawert
    # lambdabaustoff = l_objekt.baustoffid.lambdawert #alte berechnung

    uwert = (1 - 0.02 * staerkedaemmung) * lambdabaustoff / staerkeaussenwand

    # Berechnung Raumvolumen
    raumvolumen = raumhoehe * raumflaeche

    if uwert < 1.5:
        aufschlaguwert = 0
    elif uwert > 1.5 and uwert < 2.0:
        aufschlaguwert = 0.05
    elif uwert > 2.0 and uwert < 2.5:
        aufschlaguwert = 0.1
    elif uwert > 2.5 and uwert < 3.5:
        aufschlaguwert = 0.15
    elif uwert > 3.5:
        aufschlaguwert = 0.2
    else:
        print("kann uwert nicht berechnen")

    print('quali', l_objekt.fensterqualitaet)

#wenn fensterqualität NICHT angehackelt ist, danm aufschlagfenster = 0,05 * 2 rechnen
    if l_objekt.fensterqualitaet == True:
        # prozentualen gesamtaufschlag berechnen
        gesamtaufschlag = (anzfenster * aufschlagfenster) + \
                          (anzaussenwaende * aufschlagwaende) + \
                          aufschlaguwert + aufschlagueberdimensionierung - \
                          (abschlagdaemmung * staerkedaemmung)
    else:
        gesamtaufschlag = (anzfenster * aufschlagfenster*2) + \
                          (anzaussenwaende * aufschlagwaende) + \
                          aufschlaguwert + aufschlagueberdimensionierung - \
                          (abschlagdaemmung * staerkedaemmung)


    # volumenäquivalent
    volumenaequivalent = raumvolumen + raumvolumen * gesamtaufschlag

    #wird für Heizkostenberechnung gesichert, da sie sonst 2x berechnet werden muss
    sicherungvolumenaequivalent = volumenaequivalent

    anzS = 0
    anzM = 0
    anzL = 0

    while volumenaequivalent > 0:
        print("volaequ.: ", volumenaequivalent)
        if volumenaequivalent < 0:
            break
        elif volumenaequivalent <= 20:
            anzS = anzS + 1
            volumenaequivalent = volumenaequivalent - 20
        elif volumenaequivalent <= 50:
            anzM = anzM + 1
            volumenaequivalent = volumenaequivalent - 50
        elif volumenaequivalent >= 50:
            anzL = anzL + 1
            volumenaequivalent = volumenaequivalent - 75

    if l_raum.alternative:
        if anzS == 1 and anzL > 0:
            anzS = anzS - 1
            anzL = anzL - 1
            anzM = anzM + 2

    return anzS, anzM, anzL, sicherungvolumenaequivalent

def get_heizkostenabschaetzung(l_kunde, l_raum, l_objekt, winter, volumenaequivalent):

    q_bauweise = T_Bauweise.objects.get(id=l_objekt.bauweiseid)
    bauweisekennzahl = q_bauweise.energiekennzahlwert

    # Abhängig von der Bauweise werden auch Heizstunden pro Tage angenommen.
    # und Wetterbedingungen "milder" "normaler" "strenger Winter"
    # werden alle 3 berechnet
    #TODO: umbenennen von heiztagewindermild auf heizSTUNDENwintermild
    if winter == 'mild':
        #Winter normal daher 6 Heizstunden pro Tag
        heizstundenprotag = q_bauweise.heiztagewintermild
    elif winter == 'normal':
        heizstundenprotag = q_bauweise.heiztagewinternormal
    elif winter == 'streng':
        heizstundenprotag = q_bauweise.heiztagewinterstreng

    # Eingabe in Formular
    heiztage = l_kunde.heiztage

    # gewünschte Raumtemp = eingabe Formular
    raumtemp = l_kunde.raumtemp

    # stromkosten = eingabe Formular
    stromkosten = l_kunde.stromkosten

    heizkostenprojahr = (bauweisekennzahl * heizstundenprotag * heiztage) * (
                (100 + ((raumtemp - 21) * 6)) / 100) * volumenaequivalent * 0.931 * stromkosten
    # das ganze 3x berechnen mit 5/6/7

    print((bauweisekennzahl * heizstundenprotag * heiztage))
    print(((100 + ((raumtemp - 21) * 6)) / 100))
    print(volumenaequivalent * 0, 931 * stromkosten)

    kwhprojahr = heizkostenprojahr / stromkosten

    kwhprojahrproqm = kwhprojahr / volumenaequivalent / 0.931

    heizkosenpromonat = heizkostenprojahr / 12

    #gerundete Werte zurückgeben
    return round(heizkosenpromonat), round(heizkostenprojahr), round(kwhprojahrproqm), round(kwhprojahr)
