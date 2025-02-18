from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'gestion'

urlpatterns = [
    path('', views.accueil, name='accueil'),

    path('produits/', views.liste_produits, name='liste_produits'),
    path('produits/ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('produits/modifier/<int:produit_id>/', views.modifier_produit, name='modifier_produit'),
    path('produits/supprimer/<int:produit_id>/', views.supprimer_produit, name='supprimer_produit'),

    path('rechercher/', views.rechercher_produit, name='rechercher_produit'),

    path('ventes/', views.liste_ventes, name='liste_ventes'),
    path('ventes/effectuer/<int:produit_id>/', views.effectuer_vente, name='effectuer_vente'),

    path('factures/<int:facture_id>/', views.afficher_facture, name='afficher_facture'),
    path('factures/pdf/<int:facture_id>/', views.generate_pdf, name='generate_pdf'),  

    path('tableau-de-bord/', views.tableau_de_bord, name='tableau_de_bord'),

    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

    path('inscription/', views.inscription, name='inscription'),

    path('categories/', views.gestion_categories, name='gestion_categories'),
    path('categories/ajouter/', views.ajouter_categorie, name='ajouter_categorie'),
    path('categories/modifier/<int:categorie_id>/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/supprimer/<int:categorie_id>/', views.supprimer_categorie, name='supprimer_categorie'),

    path('produit/<int:produit_id>/', views.produit_detail, name='produit_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
