from django.db import models

# Create your models here.
class UserData(models.Model):
    email = models.EmailField(default='')
    PetInfo = models.JSONField(default=dict) # JSON con informacion de la mascota
    CA = models.IntegerField(default=0) # Credito ambiental
    NBA = models.IntegerField(default=0) #Nivel de Bienestar del Abmiente
    CR = models.IntegerField(default=0) #Credito Real

    def updateFromDict(self, data:dict) -> str:
        fields = list(data.keys())
        if 'NBA' in fields: self.NBA += data['NBA']
        if 'CA' in fields: self.CA += data['CA']
        if 'CR' in fields: self.CR += data['CR']
        if 'PetInfo' in fields: self.PetInfo = data['PetInfo']
        try: 
            self.save()
            return 'Actualizacion exitosa!'
        except: return 'Error en actualizacion'
        
