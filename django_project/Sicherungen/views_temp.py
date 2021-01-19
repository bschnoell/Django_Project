from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_project.angebot.forms import KundeCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required #login decorator importieren
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django_project.angebot.forms import *
from django_project.angebot.models import *

from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView
)

def richtiger_user_test_func(self):
    # über self-getObj bekommt man das aktuelle Post objekt mit dem man dann arbeiten kann
    angebot = self.get_object()
    if self.request.user == angebot.kundenid.userid:
        return True
    # durch einrückung ist return false der else zweig
    return False

#TODO: UserPassesTestMixin oder Decorator hier noch integrieren wie bei Blog Post View
#damit man nur seine eigenen angebote ändern / Läschen kann
#TODO: isValid function umschreiben und Pflichtfelder prüfen

class AngebotView(View):
    decorators = [login_required]

    @method_decorator(decorators)
  #  @user_passes_test(richtiger_user_test_func)
    def get(self, request, id=None):
        print("get Eingang")
        if id:#wenn ID = True dann Änderen EDIT VIEW
            print('get: - id: ', id, "darum ändern")

            # weil mein Ausgangspunkt ist der Kunde und dann kann ich alle anderen Daten ermitteln

            #1) Angebot holen über ID = Ausgangspunkt
            angebot = get_object_or_404(Test_Angebot, id=id)
            angebot_form = AngebotForm(instance=angebot)

            #2) Kunde holen über Kunden ID in Angebot
            kunde_form = KundeForm(instance=angebot.kundenid)

            #3) Objekte holen ist 1:n Beziehung daher mehrere Objekte möglich
            #mehrere Objekte holen da 1:n
            objekte = angebot.test_objekt_set.all()
            #eig. wird aber immer nur 1 Objekt gespeichert, daher das 1 auswählen
            #könnte hier noch dynamischer machen und drüber loopen
            #dann wirds aber kompliziert da dann zu jeden der objekte auch noch
            #mehrere Räume speicher muss, und dann irgendwie einen 2 dimensionalen
            #context generieren muss....
            objekt = objekte[0]
            objekt_form = ObjektForm(instance=objekt)

            #4) Räume aus Objekt holen
            raeume = objekt.test_raum_set.all()
            raum_forms = [RaumForm(prefix=str(
                raum.id), instance=raum) for raum in raeume]

            template = 'angebot/edit_angebot.html'

        else:#Wenn ID = None, Forms rendern für neuen Datensatz eingeben
            print("get - ID ist leer - neue Formen erzeugen")
            kunde_form = KundeForm(instance=Test_Kunde())
            angebot_form = AngebotForm(instance=Test_Angebot())
            objekt_form = ObjektForm(instance=Test_Objekt())
            #TODO: Räume dynamisch hinzufügen und entfernen
            raum_forms = [RaumForm(prefix=str(
                x), instance=Test_Raum()) for x in range(3)]
            template = 'angebot/new_angebot.html'

        context = {'kunde_form': kunde_form ,'angebot_form': angebot_form,
                   'objekt_form': objekt_form, 'raum_forms': raum_forms}
        return render(request, template, context)

#TODO: Neues Angebot- bereits angelegte Kunden auswählen oder neuen Kunden anlegen

    @method_decorator(decorators)
    def post(self, request, id=None): # Post = Speichern/Ändern
        print("post Eingang")
        context = {}
        if id:#wenn Post und ID vorhanden, dann PUT aufrufen = Vorhanden Datensatz Ändern
            print('post: id: ', id, 'id vorhanden - nun aufruf PUT')
            return self.put(request, id)

        print('post: id leer darum alles neu anlegen und speichern')
        #Forms aus Request holen
        kunde_form = KundeForm(request.POST, instance=Test_Kunde())
        angebot_form = AngebotForm(request.POST, instance=Test_Angebot())
        objekt_form = ObjektForm(request.POST, instance=Test_Objekt())
        heizkostenabschaetzungraum_form = HeizkostenabschaetzungraumForm(request.POST, instance=T_Heizkostenabschaetzung_Raum())
       # print('Baustoff:', objekt_form.cleaned_data.get('baustoff'))
        raum_forms = [RaumForm(request.POST, prefix=str(
            x), instance=Test_Raum()) for x in range(0, 3)]

        #wenn die Eingabe der Formen passt
        if kunde_form.is_valid() and angebot_form.is_valid() \
                and objekt_form.is_valid() and all([cf.is_valid() for cf in raum_forms]):
            print('post: alles valid darum jetzt alles speichern')

            new_kunde = kunde_form.save(commit=False)
            new_kunde.userid = request.user #Fremdschlüssel setzen

            new_kunde.save()

            new_angebot = angebot_form.save(commit=False)
            new_angebot.kundenid = new_kunde#Fremdschlüssel der gerade gespeicherte Kunde
          #  new_angebot.titel = angebot_form.cleaned_data.get('titel')
            new_angebot.save()

            new_objekt = objekt_form.save(commit=False)
            new_objekt.angebotid = new_angebot#Fremdschlüssel der gerade gespeicherte Kunde
            new_objekt.save()

            #Heitkostenabschätzung mitspeichern, obwohl nichts übernommen wird.
            new_heizkostenabschaetzungraum = heizkostenabschaetzungraum_form.save(commit=False)
            new_heizkostenabschaetzungraum.angebot = new_angebot#Fremdschlüssel der gerade gespeicherte Kunde
            new_heizkostenabschaetzungraum.save()

            for cf in raum_forms:
                new_raum = cf.save(commit=False)
                new_raum.objektid = new_objekt
                new_raum.anzS, new_raum.anzM, new_raum.anzL  = self.get_anz_heizkoerper(new_raum, new_objekt)

                new_raum.save()

            messages.success(request, 'Angebot wurde gespeichert!')
            return HttpResponseRedirect(reverse('angebot:angebot_details', kwargs={'id': new_angebot.id}))

        else:
            print("kunde:", kunde_form.errors)
            print("angebot:", angebot_form.errors)
            print("objekt", objekt_form.errors)
            for rf in raum_forms:
                print("raum:", rf.errors)

        context = {'angebot_form': angebot_form, 'kunde_form': kunde_form,
                   'objekt_form': objekt_form, 'raum_forms': raum_forms}

        return render(request, 'angebot/new_angebot.html', context)


    @method_decorator(decorators)
    def put(self, request, id=None): #vorhandenen Datensatz ändern
        print("put Eingang = Edit Speichern")
        context = {}

        #1) Angebot
        angebot = get_object_or_404(Test_Angebot, id=id)
        angebot_form = AngebotForm(request.POST, instance=angebot)

        # 2) Kunde holen über Kunden ID in Angebot
#        kunde_form = KundeForm(instance=angebot.kundenid)
        kunde_form = KundeForm(request.POST, instance=angebot.kundenid)

        # 3) Objekte holen ist 1:n Beziehung daher mehrere Objekte möglich
        objekte = angebot.test_objekt_set.all()
        objekt = objekte[0]
        #objekt_form = ObjektForm(instance=objekt)
        objekt_form = ObjektForm(request.POST, instance=objekt)

        # 4) Räume aus Objekt holen
        raeume = objekt.test_raum_set.all()
        raum_forms = [RaumForm(request.POST, prefix=str(raum.id), instance=raum) for raum in raeume]

        if kunde_form.is_valid() and angebot_form.is_valid() \
                and objekt_form.is_valid() and all([cf.is_valid() for cf in raum_forms]):

            new_kunde = kunde_form.save(commit=False)
            new_kunde.save()

            new_angebot = angebot_form.save(commit=False)
            new_angebot.save()

            new_objekt = objekt_form.save(commit=False)
            new_objekt.save()

            for rf in raum_forms:
                new_raum = rf.save(commit=False)
                new_raum.anzS, new_raum.anzM, new_raum.anzL  = self.get_anz_heizkoerper(new_raum, new_objekt)
                new_raum.save()

            messages.success(request, 'Angebot wurde erfolgreich geändert!')
            return HttpResponseRedirect(reverse('angebot:angebot_details', kwargs={'id': new_angebot.id}))

        else:
            messages.warning(request, 'Eingabe - Invalid')

        context = {'angebot_form': angebot_form, 'kunde_form': kunde_form,
                   'objekt_form': objekt_form, 'raum_forms': raum_forms}

        return render(request, 'angebot/edit_angebot.html', context)

# TODO: Delete testen und ausprogrammieren
    @method_decorator(decorators)
    def delete(self, request, id=None):
        angebot = get_object_or_404(Test_Angebot)
        angebot.delete()
        return HttpResponseRedirect('/dashboard/') # redirect zu angebot
        #return redirect('angebot_liste')
        #return HttpResponseRedirect('angebot:angebot_liste')
        #return redirect('angebot:angebot_liste')

#Berechnung des ERS Algorithmus
    def get_anz_heizkoerper(self, l_raum, l_objekt):

        volumenaequivalent = get_volumenaequivalent(l_raum, l_objekt)

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

        return anzS, anzM, anzL

def get_heizkostenabschaetzung(self, l_kunde, l_raum, l_objekt, winter):

    q_bauweise = T_Bauweise.objects.get(id=l_objekt.bauweiseid)
    bauweisekennzahl = q_bauweise.bauweisekennzahlwert

    # Abhängig von Wetterbedingungen "milder" "normaler" "strenger Winter" werden  Heizstunden pro Tage angenommen.
    # werden alle 3 berechnet
    if winter == 'mild':
        #Winter normal daher 6 Heizstunden pro Tag
        heizstundenprotag = 5
    elif winter == 'normal':
        heizstundenprotag = 6
    elif winter == 'streng':
        heizstundenprotag =  7

    # Eingabe in Formular
    heiztage = l_kunde.heiztage

    # gewünschte Raumtemp = eingabe Formular
    raumtemp = l_kunde.raumtemp

    # stromkosten = eingabe Formular
    stromkosten = l_kunde.stromkosten

    volumenaequivalent = get_volumenaequivalent(l_raum, l_objekt)

    print("volfix", volumenaequivalent)
    heizkostenprojahr = (bauweisekennzahl * heizstundenprotag * heiztage) * (
                (100 + ((raumtemp - 21) * 6)) / 100) * volumenaequivalent * 0.931 * stromkosten
    # das ganze 3x berechnen mit 5/6/7

    print((bauweisekennzahl * heizstundenprotag * heiztage))
    print(((100 + ((raumtemp - 21) * 6)) / 100))
    print(volumenaequivalent * 0, 931 * stromkosten)
    print('Heizkosten:', heizkostenprojahr)

    kwhprojahr = heizkostenprojahr / stromkosten

    print('kwhprojahr', kwhprojahr)

    kwhprojahrproqm = kwhprojahr / volumenaequivalent / 0.931

    print(kwhprojahrproqm)

    heizkosenpromonat = heizkostenprojahr / 12
    print(heizkosenpromonat)




def get_volumenaequivalent(self, l_raum, l_objekt):

    # Eingabewerte
    raumhoehe = l_raum.hoehe  # in meter
    raumflaeche = l_raum.flaeche  # in qm
    anzfenster = l_raum.anzfenster
    anzaussenwaende = l_raum.anzaussenflaechen
    staerkedaemmung = l_objekt.dickedaemmung  # in cm
    # Stärke Dämmung wird auf 12 maximal "gedeckelt"
    if staerkedaemmung > 12:
        staerkedaemmung = 12

    staerkeaussenwand = l_objekt.dickeaussenwand  # in cm

    # Fixwerte
    # mit get bekommt man immer nur einen eintrag
    q_aufschlagfenster = t_config.objects.get(art='aufschlagfenster')
    q_aufschlagwaende = t_config.objects.get(art='aufschlagwaende')
    q_aufschlagueberdimensionierung = t_config.objects.get(art='aufschlagueberdimensionierung')
    q_abschlagdaemmung = t_config.objects.get(art='abschlagdaemmung')

    aufschlagfenster = q_aufschlagfenster.wert  # 5%
    aufschlagwaende = q_aufschlagwaende.wert  # 5%
    aufschlagueberdimensionierung = q_aufschlagueberdimensionierung.wert  # 10%

    abschlagdaemmung = q_abschlagdaemmung.wert  # 2%

    # uwert Berechnung - je nach Bauweise:

    # ID/PK von Baustoff wird direkt in Objekt tabelle gespeichert, funktioniert über choices feld
    # in model.forms von objekt...
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

    # wenn fensterqualität NICHT angehackelt ist, danm aufschlagfenster = 0,05 * 2 rechnen
    if l_objekt.fensterqualitaet == True:
        # prozentualen gesamtaufschlag berechnen
        gesamtaufschlag = (anzfenster * aufschlagfenster) + \
                          (anzaussenwaende * aufschlagwaende) + \
                          aufschlaguwert + aufschlagueberdimensionierung - \
                          (abschlagdaemmung * staerkedaemmung)
    else:
        gesamtaufschlag = (anzfenster * aufschlagfenster * 2) + \
                          (anzaussenwaende * aufschlagwaende) + \
                          aufschlaguwert + aufschlagueberdimensionierung - \
                          (abschlagdaemmung * staerkedaemmung)

    # volumenäquivalent
    volumenaequivalent = raumvolumen + raumvolumen * gesamtaufschlag
    return volumenaequivalent


@login_required
def index(request):
    context = {}
    angebote = Test_Angebot.objects.all()
   # angebote = Test_Angebot.objects.filter(userid=request.user)
    context['angebote'] = angebote
    return render(request, 'angebot/angebot_index.html', context)




@login_required
def dashboard(request):
#TODO: Dashboard mit Count Angebot und Kunden siehe Mail in  HTK Django Ordern mit Yutube Link

#TODO: entweder FILTER deklarieren oder queryset von kunden drüberloopen
#und nur angebote des Kunden verwenden

    context = {}
    #eingeloggten benutzer auslesen
    user = User.objects.get(username=request.user)

    kunden = user.test_kunde_set.all()

    anz_angebote_offen = 0
    anz_angebote_verkauft = 0
    anz_angebote_nicht_verkauft = 0
    anz_angebote_gesamt = 0

    for kunde in kunden:
        anz_angebote_offen = anz_angebote_offen + kunde.test_angebot_set.filter(status='offen').count()
        anz_angebote_verkauft = anz_angebote_verkauft + kunde.test_angebot_set.filter(status='verkauft').count()
        anz_angebote_nicht_verkauft = anz_angebote_nicht_verkauft + kunde.test_angebot_set.filter(status='nicht verkauft').count()
        anz_angebote_gesamt = anz_angebote_gesamt + kunde.test_angebot_set.all().count()

  #  kunden_liste  = Test_Kunde.objects.filter(userid=request.user)
   # angebote = Test_Angebot.objects.all()

    context= {'kunden':kunden,
              'anz_angebote_offen':anz_angebote_offen,
              'anz_angebote_verkauft':anz_angebote_verkauft,
              'anz_angebote_nicht_verkauft':anz_angebote_nicht_verkauft,
              'anz_angebote_gesamt': anz_angebote_gesamt
              }

  #  context['kunden'] = kunde

    return render(request, 'angebot/angebot_dashboard.html', context)

# TODO: Rechner integrieren
#function based view
def rechner(request):#wird in urls.py aufgerufen
    return render(request, 'angebot/angebot_rechner.html', {'title': 'Rechner'}) #das dritte Argument ist der Titel der im HTML File angezeigt wird


@login_required
def details(request, id=None):
    # TODO: Details genauer ausprogrammieren
    context = {}
    try:
        angebot = Test_Angebot.objects.get(id=id)
        kunde = angebot.kundenid
        # mit .get bekommt man nur einen Eintrag (könnte also bei mehreren Objeten zu einem Fehler führen)
        objekt = Test_Objekt.objects.get(angebotid=angebot.id)
        # mit .filter bekommt man ein queryset
        raeume = Test_Raum.objects.filter(objektid=objekt.id)
    except Exception as e:
    #except Test_Raum.DoesNotExist:
        raise Http404

    context['angebot'] = angebot
    context['kunde'] = kunde
    context['objekt'] = objekt
    context['raeume'] = raeume
    return render(request, 'angebot/angebot_detail.html', context)
#TODO: Heizkostenabschätzung berechnen, sollte bei Details angezeigt und beim PDF dabei sein

"""
@login_required(login_url="/login/")
def vote_poll(request, id=None):
    context = {}
    try:
        question = Question.objects.get(id=id)
    except:
        raise Http404
    context["question"] = question

    if request.method == "POST":
        user_id = 1
        print(request.POST)
        data = request.POST
        ret = Answer.objects.create(user_id=user_id, choice_id=data['choice'])
        if ret:
            return HttpResponseRedirect(reverse('poll_details', args=[question.id]))
        else:
            context["error"] = "Your vote is not done successfully"
            return render(request, 'polls/poll.html', context)
    else:
        return render(request, 'polls/poll.html', context)
"""

####################################
#Alter Abschnitt
####################################
@login_required()
def createKunde(request):
    # wenn POST kommt dann wird der User gespeichert, wenn nur Get kommt dann nur die Seite anzeigen
    if request.method == 'POST':
        # Erzeuge neue Creation Form aber mit den Daten die schon in der alten
        # Creation Form gespeichert waren, darum wird request.Post übergeben
        # so bleibt zB der Username auch bei einer invaliden Eingabe in der Form enthalten
        #und wird unten der render methode übergeben
        kundenform = KundeCreationForm(request.POST)#in request.Post sind die Daten enthalten
        kundenform.user_id = request.user
        print("hier ", request.user, request.user.id)
        if kundenform.is_valid():
            kundenform.user_id = request.user
            print("valid")
            kundenform.save()
            projektkunde = kundenform.cleaned_data.get('projektkunde')
           #message speichern, wird in base.html ausgegeben
            messages.success(request, f'Kunde {projektkunde} wurde gespeichert!')
            #umleitung zur Home Seite, dort wird message ausgegeben
            #return redirect('angebot-liste')
            return redirect('/angebot/')
        else:
            print("not valid")
    else:#Das ist wenn GET Befehl kommt, also wenn nur Anzeige
        kundenform = KundeCreationForm()

    return render(request, 'angebot/angebot_testkunde_create.html', {'kundenform': kundenform})



#####################################
#Inlineviews Klassenmäßig test....
#####################################
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet

class TestkundeInline(InlineFormSet):
    model = Testkunde
    fields = ['vname', 'nname']

class TestangebotInline(InlineFormSet):
    model = Testangebot
    fields = ['wert1', 'wert2']


class CreateTestangebotInlineView(CreateWithInlinesView):
    model = Testkunde
    inlines = [TestangebotInline]
    fields = ['vname', 'nname']

class UpdateTestangebotInlineView(CreateWithInlinesView):
    model = Testkunde
    inlines = [TestangebotInline]

    def test_func(self):
        #über self-getObj bekommt man das aktuelle Post objekt mit dem man dann arbeiten kann
        testkunde = self.get_object()
        return True
        #durch einrückung ist return false der else zweig


    def form_valid(self, form):
        return super().form_valid(form)#retur die form ist valide, mit der form als übergabenargument




#    def form_valid(self, form):
#        return super().form_valid(form)



# Create your views here.
#@login_required()
#def angebot(request):
#   z context = {
#        'posts': Post.objects.all() #hier wird Post Model Objekt der Tabelle Post übergeben.
#    }
""""
#Funktion View für Testkundenliste Anzeige
def testkunde_list(request):
   testkunden = Testkunde.objects.all()
   return render(request,
                 'angebot/angebot.html',
                 {'testkunden': testkunden})
"""

#class based view, erbt von ListView
class TestkundeListView(ListView):
    # model gibt an was für Query Abfrage erstellt wird, es werden also alle Post Einträge herangezogen
    #mit context_object_name kann mann dann sagen welchen namen die Liste haben soll, in die eben die Post
    #Abfrage Ergebnisse gespeichert werden sollen
    model = Testkunde
    #muss ein template für den view angeben
    template_name = 'angebot/angebot.html'  # naming conventionen: <app>/<model>_<viewtype>.html also zB blog/post_form
    # wie heißt die variable, über die wir drüber loopen
    #wenn man contobjname nicht angibt wird strd. mäßig 'object' verwendet (muss man dann in html ändern)
    context_object_name = 'testkunden'
    #ordering = ['-date_posted']#das -ändert  von oldest to newest auf newest to oldest sortierung


class TestkundeDetailView(DetailView):
    model = Testkunde
    #muss ein template für den view angeben
    template_name = 'angebot/detail_angebot.html'  # naming conventionen: <app>/<model>_<viewtype>.html also zB blog/post_form
    # wie heißt die variable, über die wir drüber loopen
    #wenn man contobjname nicht angibt wird strd. mäßig 'object' verwendet (muss man dann in html ändern)
    context_object_name = 'testkunde_list'


    #zweites Model hinzufügen
    def get_context_data(self, **kwargs):
        context = super(TestkundeDetailView, self).get_context_data(**kwargs)
        print(self.object.id)
        context.update({
            #kunde = fremdschlüssel self.object.id = primary key der tabelle
            'testangebotlist': Testangebot.objects.filter(kunde=self.object.id)
        })
        return context


class TestkundeCreateView(LoginRequiredMixin, CreateView):
    model = Testkunde
    fields = ['vname', 'zahl1', 'zahl2']

#hier kann man zB noch felder zusätzlich setzen die vom db model als Muss gekennzeichne sind
    def form_valid(self, form):
        return super().form_valid(form)

#   form = UserCreationForm()
#   return render(request, 'angebot/angebot.html', {'form': form})

#nur seine eigenen postst editieren kann
class TestkundeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Testkunde
    fields = ['vname', 'zahl1', 'zahl2']

    def test_func(self):
        #über self-getObj bekommt man das aktuelle Post objekt mit dem man dann arbeiten kann
        testkunde = self.get_object()
        return True
        #durch einrückung ist return false der else zweig


    def form_valid(self, form):
        return super().form_valid(form)#retur die form ist valide, mit der form als übergabenargument


