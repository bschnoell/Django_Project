from django.db import models
from django.contrib.auth.models import User
from PIL import Image#Import um das Bild herunter komprimieren zu ermöglichen (mit PILLOW)


#Tablle für Profil des Benutzers anlegen
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)#hat 1:1 Beziehung zu User Tabelle
    #on_dele.CASCADE -> wenn user gelöscht wird, wird auch profile gelöscht, aber nicht umgekehrt
    # bei Upload wird in profile_pics gespeichert(es wird also ein Ordner Erstellt
    #und wenn noch kein FIle hochgeladen wird, dann wird default.jpg angezeigt
    image = models.ImageField(default='default.jpg', upload_to='prof1ile_pics')
    firma = models.CharField(max_length=100, default='Firma:')
    plz = models.CharField(max_length=4, default='PLZ:')
    ort = models.CharField(max_length=30, default='Ort:')
    telefonnr = models.CharField(max_length=15, default='Tel:')
    mail = models.EmailField(max_length=100, default='Mail:')
    strasse = models.CharField(max_length=100, default='Straße:')



    #bei Erzeugnug wird Benutzerame Profile angezeigt
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)#strd save methode der vorigen klassen durchlaufen

        img = Image.open(self.image.path)#img variable mit dem image der current instance belegen

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)#tuple erzeugen dass dann übergeben wird
            img.thumbnail(output_size)#mit der thumbnail kann man eben das bild komprimieren
            img.save(self.image.path)