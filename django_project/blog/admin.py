from django.contrib import admin
from .models import Post
# Register your models here.
#Hier kann die Tabellen aus der Datenbank zur Admin Seite hinzufügen

admin.site.register(Post)

