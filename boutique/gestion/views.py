from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit, Vente, Categorie
from .forms import ProduitForm, ConnexionForm, VenteForm, CategorieForm  # Ajoutez CategorieForm ici
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django.utils.crypto import get_random_string
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Facture
from django.contrib import messages
from django.http import HttpResponse


@login_required(login_url='connexion')
def accueil(request):
    produits = Produit.objects.all()
    return render(request, 'accueil.html', {'produits': produits})


@login_required(login_url='connexion')
def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'liste_produits.html', {'produits': produits})

@login_required(login_url='connexion')
def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gestion:liste_produits')
    else:
        form = ProduitForm()
    return render(request, 'ajouter_produit.html', {'form': form})

@login_required(login_url='connexion')
def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('gestion:liste_produits')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'modifier_produit.html', {'form': form})

@login_required(login_url='connexion')
def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    produit.delete()
    return redirect('gestion:liste_produits')

@login_required(login_url='connexion')
def rechercher_produit(request):
    query = request.GET.get('q')
    if query:
        produits = Produit.objects.filter(nom__icontains=query)
    else:
        produits = Produit.objects.all()
    return render(request, 'rechercher_produit.html', {'produits': produits})

@login_required(login_url='connexion')
def liste_ventes(request):
    ventes = Vente.objects.all()
    return render(request, 'liste_ventes.html', {'ventes': ventes})

@login_required(login_url='connexion')
def effectuer_vente(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save(commit=False)
            vente.produit = produit
            vente.montant_total = vente.quantite_vendue * produit.prix
            vente.save()
            return redirect('gestion:liste_ventes')
    else:
        form = VenteForm()
    return render(request, 'effectuer_vente.html', {'form': form, 'produit': produit})

@login_required(login_url='connexion')
def tableau_de_bord(request):
    total_ventes = Vente.objects.aggregate(total=Sum('montant_total'))['total']
    produits_en_rupture = Produit.objects.filter(quantite=0)
    
    if not produits_en_rupture.exists():
        produits_en_rupture = [
            Produit(nom='Produit A', quantite=0, prix=1000),
            Produit(nom='Produit B', quantite=0, prix=2000)
        ]

    return render(request, 'tableau_de_bord.html', {
        'total_ventes': total_ventes,
        'produits_en_rupture': produits_en_rupture
    })

def generate_pdf(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    template_path = 'pdf_facture.html'
    context = {'facture': facture}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{facture.numero_facture}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF : <pre>' + html + '</pre>')
    return response 


def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('gestion:accueil') 
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ConnexionForm()
    return render(request, 'connexion.html', {'form': form})

def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion:connexion')
    else:
        form = UserCreationForm()
    return render(request, 'inscription.html', {'form': form})

def deconnexion(request):
    logout(request)
    return redirect('gestion:accueil')

@login_required(login_url='connexion')
def effectuer_vente(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save(commit=False)
            vente.produit = produit
            vente.montant_total = vente.quantite_vendue * produit.prix
            vente.save()

            numero_facture = get_random_string(length=12)
            facture = Facture(vente=vente, numero_facture=numero_facture)
            facture.save()

            vente.facture = facture
            vente.save()

            return redirect('gestion:afficher_facture', facture_id=facture.id)
    else:
        form = VenteForm()
    return render(request, 'effectuer_vente.html', {'form': form, 'produit': produit})


@login_required(login_url='connexion')
def afficher_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    return render(request, 'afficher_facture.html', {'facture': facture})


@login_required(login_url='connexion')
def gestion_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'gestion_categories.html', {'categories': categories})

@login_required(login_url='connexion')
def ajouter_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion:gestion_categories')
    else:
        form = CategorieForm()
    return render(request, 'ajouter_categorie.html', {'form': form})

@login_required(login_url='connexion')
def modifier_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            return redirect('gestion:gestion_categories')
    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'modifier_categorie.html', {'form': form})

@login_required(login_url='connexion')
def supprimer_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    categorie.delete()
    return redirect('gestion:gestion_categories')

@login_required(login_url='connexion')
def produit_detail(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    return render(request, 'produit_detail.html', {'produit': produit})

