from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LogRegForm, UpdateForm
from .models import UserData, Item, LeaderBoard
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import datetime
import qrcode
import qrcode.image.svg
from io import BytesIO
import jwt
import bcrypt
import json
import os
from dotenv import load_dotenv
load_dotenv()
# SECRET KEYS
SALT_KEY = os.getenv('SALT_KEY').encode()
AUTHLEVELKEYS = {
    'USER_LEVEL_KEY': os.getenv('USER_LEVEL_KEY').encode(),
    'SUPER_LEVEL_KEY': os.getenv('SUPER_LEVEL_KEY').encode(),
}


# QR
def QrCode(request, ssid):
    id, username = getUserIDBySSID(ssid)
    ctx = {'ssid':ssid, 'username':username}
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(id, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    ctx["svg"] = stream.getvalue().decode().replace('svg:','').replace('mm','vmin')
    return render(request, "qrcode.html", ctx)

def QrCodeScan(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not (isValid and auth): return redirect('/msg/la_sesion_ya_no_es_valida')
    ctx = {'ssid':ssid}
    return render(req, 'scan.html', ctx)

def NoQrForm(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not (isValid and auth): return redirect('/msg/la_sesion_ya_no_es_valida')
    ctx = {'ssid':ssid}
    return render(req, 'noscan.html', ctx)

def UpdateUser(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not (isValid and auth): return redirect('/msg/la_sesion_ya_no_es_valida')
    if req.method != 'POST': redirect(f'/scanmsg/{ssid}/metodo_no_valido')
    formData = UpdateForm(req.POST).clean()
    if formData['isScan']: target = UserData.objects.get(id=formData['userID'])
    else: target = UserData.objects.get(email=formData['email'])
    msg = target.updateFromDict(formData)
    return redirect(f'/scanmsg/{ssid}/{msg}')

# ACTIONS.
def newUser(email, passw):
    User.objects.create_user(
        email, email, passw, last_login=datetime.datetime.now()
    ).save() #hash
    UserData.objects.create(
        email=email,
        PetInfo={# JSON con informacion de la mascota
            'name':'pedro',
            'tipo':'gato',
            'estado':'normal',
        },
        CR=0,
        NBA=0,
        CA=0,
        Items='{}'
    ).save() #data

def findUserAuthLevel(user:str) -> int:
    '''Busca el valor is_superuser en la base de datos'''
    value = User.objects.get(email=user).is_superuser
    return int(value)

def generateAuthKey(user:str, authlevel:int) -> bytes:
    '''user -> email ; authlevel -> is_superuser
    Retorna el nombre de usuario hasheado por una clave que le asigna el nivel de autorizacion'''
    key = 'USER_LEVEL_KEY' if authlevel == 0 else 'SUPER_LEVEL_KEY'
    forHash = (bcrypt.gensalt(12).decode()+user).encode()
    auhtKey = bcrypt.hashpw(AUTHLEVELKEYS[key], forHash)
    return auhtKey

def validarAuthKey(AuthKey:bytes) -> list:
    isValidUser = bcrypt.checkpw(AUTHLEVELKEYS['USER_LEVEL_KEY'], AuthKey)
    isValidAdmin = bcrypt.checkpw(AUTHLEVELKEYS['SUPER_LEVEL_KEY'], AuthKey)
    isValid = isValidAdmin or isValidUser
    return [isValid, int(isValidAdmin)]

def ItemlistFromDict(d):
    lCA = list()
    lCR = list()
    keys = d.items()
    for item in keys:
        for _ in range(item[1]): 
            i = Item.objects.get(name=item[0])
            if i.tipo == 'CA': lCA.append(i.img)
            else: lCR.append(i.img)
    return { 'CA':lCA, 'CR':lCR }

def getUserIDBySSID(ssid:str) -> tuple[int, str]:
    res = jwt.decode(
            ssid,
            SALT_KEY,
            "HS256"
        )
    userPrimaryKey = UserData.objects.get(email=res['user']).pk
    return userPrimaryKey, res['user']

def getUserCR_CA_BySSID(ssid:str) -> tuple[int, int]:
    '''retorna (CR, CA)'''
    res = jwt.decode(
        ssid,
        SALT_KEY,
        "HS256"
    )
    user = UserData.objects.get(email=res['user'])
    return user.CR, user.CA

def procesarCompra(POST, ssid):
    try: item = POST['itemname']
    except: return
    res = jwt.decode(
        ssid,
        SALT_KEY,
        "HS256"
    )
    user = UserData.objects.get(email=res['user'])
    dbItem = Item.objects.get(name=item)        
    user.updateFromDict({
        dbItem.tipo: - dbItem.cost,
        'Items':dbItem,
        'NBA':dbItem.nba
    })

def getUserDataBySSID(ssid):
    '''retorna el modelo (UserData, PetData, ItemsData)'''
    res = jwt.decode(
        ssid,
        SALT_KEY,
        "HS256"
    )
    userData = UserData.objects.get(email=res['user'])
    return ( userData, userData.PetInfo, userData.Items )

def updatePet(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not isValid: return redirect('/msg/la_sesion_ya_no_es_valida')
    if req.method != 'POST': redirect('/msg/metodo_no_valido')
    queryDict = req.POST
    user, _, _ = getUserDataBySSID (ssid)
    if queryDict['name']: name = queryDict['name']
    else: name = user.PetInfo['name']
    user.updateFromDict({
        'PetInfo':{
            'name':name,
            'tipo':queryDict['tipo'],
            'estado':queryDict['estado']
        }
    })
    return redirect(f'/menu/{ssid}')


def getItems():
    '''Retorna una diccionario de listas {"CA":[], "CR":[]}
    con los items disponibles de la forma {
        "id":int,
        "name"str,
        "cost":int,
        "img":str,
        "tipo":str(CA o CR)
    }
    '''
    CA = [ el.get_clean() for el in Item.objects.filter(tipo='CA') ]
    CR = [ el.get_clean() for el in Item.objects.filter(tipo='CR') ]
    return {'CA':CA, 'CR':CR}

def createSSID(user:str) -> str:
    is_superuser = findUserAuthLevel(user)
    token = jwt.encode(
            {
            'user':user,
            'auth':generateAuthKey(user, is_superuser).decode()
            },
        SALT_KEY,
        "HS256"
        )
    return token

def validarSSID(ssid) -> list:
    try:
        res = jwt.decode(
            ssid,
            SALT_KEY,
            "HS256"
        )
        info = validarAuthKey(res['auth'].encode())
    except: info = [False, 0]
    return info

def validarCred(req):
    if req.method != 'POST':return redirect('/msg/metodo_no_valido')
    cred = req.POST['creds']
    isValid, auth = validarSSID(cred)
    if not isValid: return redirect('/msg/la_sesion_ya_no_es_valida')

    return (redirect('/menu/%s'%cred) if not auth else redirect('/panel/%s'%cred))


def recompensas(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not isValid: return redirect('/msg/la_sesion_ya_no_es_valida')
    if req.method != 'POST':return redirect('/msg/metodo_no_valido')
    user, _, _ = getUserDataBySSID(req.POST['ssid'])
    LeaderBoard.checkNewScore(user.email.split('@')[0], req.POST['time'])
    if int(req.POST['CA']) != 0:user.updateFromDict({'CA': int(req.POST['CA'])})

    return redirect(f'/gameselect/{ssid}')

# VIEWS.
def validarForm(req):
    if req.method != 'POST':return redirect('/msg/request_not_valid')
    form = LogRegForm(req.POST)
    if not form.is_valid(): return redirect('/msg/campos_no_validos')
    data = form.clean()
    try: user = User.objects.get(email=data['email'])
    except: return redirect('/msg/usuario_no_encontrado')

    if not check_password(data['contra'], user.password): return redirect('/msg/email_o_contraseña_incorrecta')
    
    ssid = createSSID(data['email'])
    
    return (redirect('/menu/%s'%ssid) if not user.is_superuser else redirect('/panel/%s'%ssid))

def validarRegistro(req):
    if req.method != 'POST':return redirect('/msg/request_not_valid')
    form = LogRegForm(req.POST)
    if not form.is_valid(): return redirect('/msg/campos_no_validos')
    data = form.clean()
    if len(User.objects.filter(email=data['email'])) != 0: return redirect('/msg/usuario_ya_existe')
    newUser(data['email'], data['contra'])

    ssid = createSSID(data['email'])

    return redirect('/perzomascota/%s'%ssid)


#No match page
'''
def unMatch(req, exc):
    ctx = { 'errorUrl':exc }
    return render( req, 'nopage.html', ctx, status=404 )

def th(req):
    ctx = { 'errorUrl':'exc' }
    return render( req, 'nopage.html', ctx, status=500 )
'''