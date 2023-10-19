from django.db import models
import json

# Create your models here.
class UserData(models.Model):
    email = models.EmailField(default='')
    PetInfo = models.JSONField(default=dict) # JSON con informacion de la mascota
    CA = models.IntegerField(default=0) # Credito ambiental
    NBA = models.IntegerField(default=0) #Nivel de Bienestar del Abmiente
    CR = models.IntegerField(default=0) #Credito Real
    Items = models.CharField(default='{}',max_length=9999)

    def updateFromDict(self, data:dict) -> str:
        '''
        NBA -> int\n
        CA -> int\n
        CR -> int\n
        PetInfo -> full dict\n
        Items -> str\n
        '''
        fields = list(data.keys())
        if 'NBA' in fields: self.NBA += data['NBA']
        if 'CA' in fields and self.CA >= -data['CA']: self.CA += data['CA']
        if 'CR' in fields and self.CR >= -data['CR']: self.CR += data['CR']
        if 'PetInfo' in fields: self.PetInfo = data['PetInfo']
        if 'Items' in fields and ( ('CR' in fields and self.CR >= -data['CR']) or ('CA' in fields and self.CA >= -data['CA']) ):
            temp = json.loads(self.Items)
            if data['Items'] not in temp: temp[data['Items']] = 1
            else: temp[data['Items']] += 1
            self.Items = json.dumps(temp)
        try: 
            self.save()
            return 'Actualizacion exitosa!'
        except: return 'Error en actualizacion'
    
        

class Item(models.Model):
    name = models.CharField(max_length=20, null=False)
    cost = models.IntegerField(default=0, null=False)
    img = models.CharField(max_length=100,default='/static/img/example/item.png')
    tipo = models.CharField(max_length=2, default='CA')
    
    def get_clean(self):
        return {
            'name':self.name,
            'cost':self.cost,
            'img':self.img,
            'tipo':self.tipo
        }