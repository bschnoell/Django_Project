"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views#vorgefertigter view für login/logout
from django.conf import settings#Einstellungen für static Media Files
from django.conf.urls.static import static#Einstellungen für static Media Files
from users import views as user_views
from angebot import views as angebot_views


#Wenn die App ein eigenes URL File hat dann mit include einbinden
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register,name='register'),#view aus user klasse mit register funktion
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),#class based views-in as_view funktion wird angegeben wo das html template liegt
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),#class based views
    path('', include('angebot.urls', namespace='angebot')),#view funktionsaufruf der in angebot app in views.py erstellt wurde
    path('blog/', include('blog.urls')),
]

#WEnn wir in Debug Mode sind(also während der Entwicklung), also nicht in Deployment
#Einstellung um die Bilder anzuzeigen
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

