from django.shortcuts import render, redirect
from .forms import LogRegForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

def validarRegistro(req):
    if req.method != 'POST':return redirect('/error')
    form = LogRegForm(req.POST)
    if not form.is_valid(): return redirect('/msg/form_not_valid')
    data = form.clean()
    if len(User.objects.filter(email=data['email'])) != 0: return redirect('/msg/usuario_ya_existe')
    User.objects.create_user(data['email'], data['email'], data['contra']).save()
    return redirect('/menu')


# Create your views here.
def validarForm(req):
    if req.method != 'POST':return redirect('/error')
    form = LogRegForm(req.POST)
    if not form.is_valid(): return redirect('/error')
    data = form.clean()

    user = User.objects.get(email=data['email'])

    if not check_password(data['contra'], user.password): return redirect('/error')
    
    return redirect('/menu')