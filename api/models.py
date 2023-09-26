from django.db import models

# Create your models here.
class UserData(models.Model):
    email = models.EmailField(default='')
    AliasM = models.CharField(max_length=20) # Alias de la Mascota
    creditos = models.IntegerField()
    NBA = models.IntegerField() #Nivel de Bienestar del Abmiente