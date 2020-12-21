from django.urls import path
#views aus der views.py file importieren
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from . import views



urlpatterns = [
    #strd classbased view für die home seite wo alle posts stehen
    path('postlist', PostListView.as_view(), name='blog-home'),
    #urlpattern mit variable erstellen post/1/ oder post/2/...<int:primary key> wird hier verwendet
    #kann anstatt von pk auch eine andere variable verwendet, muss dass dann aber beim classview angeben.
    #PK ist also strd naming convention von django
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
   #das war der Aufruf für den alten views.home function view, wurde durch classbased view ersetzt
    #path('', views.home, name='blog-home'),#views.home wurde in views.py file erzeugt
    path('about/', views.about, name='blog-about'),#views.home wurde in views.py file erzeugt
]


""""


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]

urlpatterns = [
    #strd classbased view für die home seite wo alle posts stehen
    path('', PostListView.as_view(), name='blog-home'),
    #urlpattern mit variable erstellen post/1/ oder post/2/...<int:primary key> wird hier verwendet
    #kann anstatt von pk auch eine andere variable verwendet, muss dass dann aber beim classview angeben.
    #PK ist also strd naming convention von django
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
   #das war der Aufruf für den alten views.home function view, wurde durch classbased view ersetzt
    #path('', views.home, name='blog-home'),#views.home wurde in views.py file erzeugt
    path('about/', views.about, name='blog-about'),#views.home wurde in views.py file erzeugt
]

"""

