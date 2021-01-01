from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm #authentification form importieren
#eigene Erzeugte Klassen aus forms.py importieren UserRegisterForm importieren,
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
#Decoratoren sind dazu da um für existierende Funktionen zusätzliche Funtionen hinzuzufügen
from django.contrib.auth.decorators import login_required #login decorator importieren

#view für Register
def register(request):
    # wenn POST kommt dann wird der User gespeichert, wenn nur Get kommt dann nur die Seite anzeigen
    if request.method == 'POST':
        # Erzeuge neue Creation Form aber mit den Daten die schon in der alten
        # Creation Form gespeichert waren, darum wird request.Post übergeben
        # so bleibt zB der Username auch bei einer invaliden Eingabe in der Form enthalten
        #und wird unten der render methode übergeben
        form = UserRegisterForm(request.POST)#in request.Post sind die Daten enthalten
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
           #message speichern, wird in base.html ausgegeben
            messages.success(request, f'Your Account {username} has been created! You are now able to login!')#WIRD nur einmal angezeigt wenn user erstellt wird
            #umleitung zur Home Seite, dort wird message ausgegeben
            return redirect('login')
    else:#Das ist wenn GET Befehl kommt, also wenn nur Anzeige
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


#view für Profil
@login_required
#bekommt dn request bei der funktion übergeben. Über request kann man unterscheiden ob POST = Update oder
#übermittlung von Daten oder nur GET = Anzeige von Daten
def profile(request):
    if request.method == 'POST':#post wird submittet wenn mit update button neue Daten übermittelt werden sollen
        #instanz u_form und p_form von den Klassen in forms.py erzeugen
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    #else Zweig wenn nur Get kommt, also bei der ersten Anzeige der HTML Seite wo noch keine Daten geändert wurden
    else:
        u_form = UserUpdateForm(instance=request.user)#mit request.user wird der aktuelle user übergeben der bereits eingeloggt ist
        p_form = ProfileUpdateForm(instance=request.user.profile)#hier wird das user profil vom aktuell eingeloggzen user übergeben
#die Instanzen werden dem Context übergeben, damit sie im HTML Template übergeben werden können.
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
