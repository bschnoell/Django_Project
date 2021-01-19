from django.urls import path
from . import views as angebot_views


app_name = 'angebot'

urlpatterns = [
    #path('', angebot_views.testkunde_list, name='testkunde_list'), #der name wird im HTML (Base DOkument verwendet um die URL zu finden
  #alt:  path('', angebot_views.TestkundeListView.as_view(), name='angebot-liste'),
  #  path('<int:pk>/', angebot_views.TestkundeDetailView.as_view(), name='angebot-detail'),
 #   path('new/', angebot_views.TestkundeCreateView.as_view(), name='angebot-create'),
 #   path('newTest/', angebot_views.CreateTestangebotInlineView.as_view(), name='angebot-create-inline'),
 #   path('<int:pk>/update/', angebot_views.TestkundeUpdateView.as_view(), name='angebot-update'),
  #  path('<int:pk>/updateTest/', angebot_views.UpdateWithInlinesView.as_view(), name='angebot-update-test'),
  #  path('newKunde/', angebot_views.createKunde, name='kunde-create'),  # view aus user klasse mit register funktion

    path('', angebot_views.dashboard, name='angebot_dashboard'),
    path('dashboard/', angebot_views.dashboard, name='angebot_dashboard'),
    path('add/', angebot_views.AngebotView.as_view(), name='angebot_add'),
    path('<int:id>/edit/', angebot_views.AngebotView.as_view(), name='angebot_edit'),
    path('<int:id>/delete/', angebot_views.AngebotView.as_view(), name='angebot_delete'),
    path('<int:id>/details/', angebot_views.details, name="angebot_details"),
    path('rechner/', angebot_views.rechner, name='angebot_rechner'),
    path('<int:id>/pdf/', angebot_views.generate_pdf_view, name='angebot_pdf'),
]

#TODO: PDF Angebot Creation anschauen

"""
urlpatterns = [
    #path('', angebot_views.testkunde_list, name='testkunde_list'), #der name wird im HTML (Base DOkument verwendet um die URL zu finden
    path('', angebot_views.TestkundeListView.as_view(), name='angebot-liste'),
    path('<int:pk>/', angebot_views.TestkundeDetailView.as_view(), name='angebot-detail'),
    path('new/', angebot_views.TestkundeCreateView.as_view(), name='angebot-create'),
    path('newTest/', angebot_views.CreateTestangebotInlineView.as_view(), name='angebot-create-inline'),
    path('<int:pk>/update/', angebot_views.TestkundeUpdateView.as_view(), name='angebot-update'),
    path('<int:pk>/updateTest/', angebot_views.UpdateWithInlinesView.as_view(), name='angebot-update-test'),
    path('newKunde/', angebot_views.createKunde, name='kunde-create'),  # view aus user klasse mit register funktion

    path('liste/', angebot_views.index, name='angebot_liste'),
    path('add/', angebot_views.AngebotView.as_view(), name='angebot_add'),
    path('<int:id>/edit/', angebot_views.AngebotView.as_view(), name='angebot_edit'),
    path('<int:id>/delete/', angebot_views.AngebotView.as_view(), name='angebot_delete'),
    path('<int:id>/details/', angebot_views.details, name="angebot_details"),
]
"""