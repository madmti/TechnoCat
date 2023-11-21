from django.db import models
import json

# Create your models here.
class UserData(models.Model):
    email = models.EmailField(default='')
    PetInfo = models.JSONField(default=dict) # JSON con informacion de la mascota
    CA = models.IntegerField(default=0) # Credito ambiental
    NBA = models.IntegerField(default=0) #Nivel de Bienestar del Abmiente
    CR = models.IntegerField(default=0) #Credito Real
    Items = models.JSONField(default=dict,max_length=9999)

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
            if data['Items'] not in self.Items: self.Items[data['Items']] = 1
            else: self.Items[data['Items']] += 1
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

class LeaderBoard(models.Model):
    name = models.CharField(max_length=20, null=False)
    seg = models.IntegerField(default=0, null=False)

    def get_Top():
        Objs = LeaderBoard.objects.all().order_by('seg').reverse()
        if len(Objs) <= 5: return Objs
        return Objs[:5]

    def checkNewScore(name, score):
        try:user = LeaderBoard.objects.get(name=name)
        except:user = LeaderBoard(name=name)
        if user.seg >= int(score): return
        user.seg = int(score)
        user.save()
        