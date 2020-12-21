from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile #Profil importieren



#eigene Forms Klasse erzeugen, die von der originalen Klasse erbt, und dann werden
#zusätzliche Felder hinzugefügt
#Super klassisches Beispiel von Vererbung
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


#Erbt von forms.Modelform und ändert nur Mail und Username
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

#Um das Profilbild zu ändern
class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'firma','plz','ort','telefonnr','strasse']
