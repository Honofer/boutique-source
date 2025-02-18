from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    categories = models.ManyToManyField(Categorie)
    quantite = models.IntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='produits/', null=True, blank=True) 

    def __str__(self):
        return self.nom

class Vente(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite_vendue = models.IntegerField()
    date_vente = models.DateTimeField(auto_now_add=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Vente de {self.produit.nom}"

class Facture(models.Model):
    vente = models.OneToOneField(Vente, on_delete=models.CASCADE, related_name='facture')
    numero_facture = models.CharField(max_length=100, unique=True)
    date_emission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero_facture
