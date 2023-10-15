from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LogRegForm
from .models import UserData
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import datetime
import qrcode
import qrcode.image.svg
from io import BytesIO
import jwt
import bcrypt
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
def QrCode(request, id):
    ctx = {}
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(id, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    ctx["svg"] = stream.getvalue().decode().replace('svg:','').replace('mm','vh')
    return render(request, "qrcode.html", ctx)

def QrCodeScan(req, ssid):

    return render(req, 'scan.html', {})

def UpdateUser(req, data):
    return HttpResponse('a')

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
    ).save() #data

def findUserAuthLevel(user:str) -> int:
    '''Busca el valor is_superuser en la base de datos'''
    value = User.objects.get(email=user).is_superuser
    return int(value)

def generateAuthKey(user:str, authlevel:int) -> bytes:
    '''user -> email ; authlevel -> is_superuser
    Retorna el nombre de usuario hasheado por una clave que le asigna el nivel de autorizacion'''
    userEncode = user.encode()
    key = 'USER_LEVEL_KEY' if authlevel == 0 else 'SUPER_LEVEL_KEY'
    AuthKey = bcrypt.hashpw(userEncode, AUTHLEVELKEYS[key])
    return AuthKey

def validarAuthKey(user:str, AuthKey:bytes) -> list:
    userEncode = user.encode()
    isValid = bcrypt.checkpw(userEncode, AuthKey)
    AuthLevel = findUserAuthLevel(user)
    return [isValid, AuthLevel]

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
        info = validarAuthKey(res['user'], res['auth'].encode())
    except: info = [False, 0]
    return info

def validarCred(req):
    if req.method != 'POST':return redirect('/msg/metodo_no_valido')
    cred = req.POST['creds']
    isValid, auth = validarSSID(cred)
    if not isValid: return redirect('/msg/la_sesion_ya_no_es_valida')

    return (redirect('/menu/%s'%cred) if not auth else redirect('/panel/%s'%cred))


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