from django.contrib import admin
from django.urls import path, include
from gestion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', views.connexion, name='connexion'),  
    path('accueil/', views.accueil, name='accueil'),
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('gestion/', include('gestion.urls')),  
    path('produit/<int:produit_id>/', views.produit_detail, name='produit_detail'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
