from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User #User Klasse importieren
from django.urls import reverse

#Hier wird Tabelle Post erstellt
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) #timezone.now ist eine funktion, aber hier keine () am Ende, hier wird nur der name der funktion übergeben
    author = models.ForeignKey(User, on_delete=models.CASCADE) #User ist die Fremde Tabelle - mit Cascade werden auch zusammenhängende Posts gelöscht


#Muss python manage.py makemigrations laufen lassen damit die Tabelle erstellt wird.
#dort werden unter dem Verzeichnis migrations dann die enstprechenden Files angelegt

#ist wie contructor in Java - sollte den Titel zurückgeben wenn ein Objekt erstellt wird
#dann wird in shell bei Post.objects.all() der Titel des Objektes angezeigt
    def __str__(self):
        return self.title

#reverse methode ist wie redirect, nur dass sie eine entsprechende URL als string zurückgibt
    #in unserem fall ist get_absoute_url dazu da, damit der view weiss, wo er nach dem posten
    #eines neuen blogposts redirecten soll, in unserem fall zu Postdetail mit der id-Primary key
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})