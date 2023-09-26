from django.db import models

# Create your models here.
class UserData(models.Model):
    email = models.EmailField(default='')
    AliasM = models.CharField(max_length=20) # Alias de la Mascota
    CA = models.IntegerField(default=0) # Credito ambiental
    NBA = models.IntegerField(default=0) #Nivel de Bienestar del Abmiente
    CR = models.IntegerField(default=0) #Credito Real