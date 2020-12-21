from django.db.models.signals import post_save#Post Save Signal feuern wenn User gespeichert wird
from django.contrib.auth.models import User#User Model ist der Sender - Sendet Signal
from django.dispatch import receiver#Empfänger - der Das Signal empfängt
from .models import Profile#Profil Tabelle importieren

#Funktion erstellt ein Profil für jeden Benutzerre
#receiver ist ein Decorator- Signal ist post_save - Sender ist der User
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):#Bei Senden wird User instanz und created Datum übergeben
    if created:
        Profile.objects.create(user=instance)

#das erzeugte Profil muss auch noch gespeichert werden
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()