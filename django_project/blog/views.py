from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

#function based views... es gibt aber auch class based views
def home(request):#wird in urls.py aufgerufen
    context = {
        'posts': Post.objects.all() #hier wird Post Model Objekt der Tabelle Post übergeben.
    }
    return render(request, 'blog/home.html', context)

#class based view, erbt von ListView
class PostListView(ListView):
    # model gibt an was für Query Abfrage erstellt wird, es werden also alle Post Einträge herangezogen
    #mit context_object_name kann mann dann sagen welchen namen die Liste haben soll, in die eben die Post
    #Abfrage Ergebnisse gespeichert werden sollen
    model = Post
    #muss ein template für den view angeben
    template_name = 'blog/home.html'  # naming conventionen: <app>/<model>_<viewtype>.html also zB blog/post_form
    # wie heißt die variable, über die wir drüber loopen
    #wenn man contobjname nicht angibt wird strd. mäßig 'object' verwendet (muss man dann in html ändern)
    context_object_name = 'posts'
    ordering = ['-date_posted']#das -ändert  von oldest to newest auf newest to oldest sortierung

#view für einen einzelnen Post
#nur so wenig übergabeparameter weil der rest der Übergabeparameter als strd gelassen werden
#URL Pattern muss in urls.py für diesen View natürlich auch angegeben werden
class PostDetailView(DetailView):
    model = Post
    # naming conventionen: <app>/<model>_<viewtype>.html also hier blog/post_detail
    #context_object_name = '...' wird hier nicht angegeben, dadurch wird als strd. der name 'object' verwendet

#neue Post erzeugen
#loginrequmixin ist dazu da, dass man nur posten kann, wenn man eingeloggt ist, ansonsten wird man zur
#loginpage umgeleitet
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    #felder angeben welche in dem view verwendet werden sollen
    #date und author gehen automatisch
    fields = ['title', 'content']

#form valid methode überschreiben, den author mit dem aktuell eingeloggten author setzen
#sonst kann man keinen post speichern
    def form_valid(self, form):
        #über form.instance.author kann man den author für die form setzen (ist im post model ein "Muss"-Feld, und mit self.request.user
        # bekommt man den aktuell eingeloggten benutzer
        form.instance.author = self.request.user
        #form_Valäuft sowieso, aber dadurch dass wir sie überschreiben läuft sie erst nachdem der author 
        #gesetzt wurde
        return super().form_valid(form)

#userpassesmixin ist damit man test function implementieren kann
#in der testfunktion kann man eben dan zB testen ob auch der richtige User eingeloggt ist, damit er
#nur seine eigenen postst editieren kann
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)#retur die form ist valide, mit der form als übergabenargument

    def test_func(self):
        #über self-getObj bekommt man das aktuelle Post objekt mit dem man dann arbeiten kann
        post = self.get_object()
        if self.request.user == post.author:
            return True
        #durch einrückung ist return false der else zweig
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'#wird auf die homepage gesendet wenn delete erfolgreich war

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



#function based view
def about(request):#wird in urls.py aufgerufen
    return render(request, 'blog/about.html', {'title': 'About'}) #das dritte Argument ist der Titel der im HTML File angezeigt wird







