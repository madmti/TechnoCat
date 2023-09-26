from django.shortcuts import render, redirect
from .forms import LogRegForm
from .models import UserData
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import datetime

# ACTIONS.
def newUser(email, passw):
    User.objects.create_user(
        email, email, passw, last_login=datetime.datetime.now()
    ).save() #hash
    UserData.objects.create(
        email=email,
        AliasM='Pedro', # Alias default de la mascota
        creditos=0,
        NBA=0
    ).save() #data


# VIEWS.
def validarForm(req):
    if req.method != 'POST':return redirect('/msg/request_not_valid')
    form = LogRegForm(req.POST)
    if not form.is_valid(): return redirect('/msg/campos_no_validos')
    data = form.clean()

    user = User.objects.get(email=data['email'])

    if not check_password(data['contra'], user.password): return redirect('/msg/email_o_contraseña_incorrecta')
    
    ssid = '1234'
    
    return (redirect('/menu/%s'%ssid) if not user.is_superuser else redirect('/panel/%s'%ssid))

def validarRegistro(req):
    if req.method != 'POST':return redirect('/msg/request_not_valid')
    form = LogRegForm(req.POST)
    if not form.is_valid(): return redirect('/msg/campos_no_validos')
    data = form.clean()
    if len(User.objects.filter(email=data['email'])) != 0: return redirect('/msg/usuario_ya_existe')
    newUser(data['email'], data['contra'])
    return redirect('/menu')