from django.shortcuts import render, redirect
from api.views import validarSSID


def menu(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not isValid: return redirect('/msg/la_sesion_ya_no_es_valida')
    ctx = {
        'ssid':ssid
    }
    return render( req, 'menu.html', ctx )

def landing(req, msg=''):
    ctx = { 'msg':msg if msg=='' else msg.replace('_', ' ') }
    return render( req, 'landing.html', ctx )

def panel(req, ssid, msg=''):
    isValid, auth = validarSSID(ssid)
    if not (isValid and auth): return redirect('/msg/la_sesion_ya_no_es_valida')
    ctx = {'ssid':ssid, 'msg':msg.replace('_',' ')}
    return render( req, 'panel.html', ctx )


def PerzoMascota(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not isValid: return redirect('/msg/la_sesion_ya_no_es_valida')
    ctx = {
        'petName':'pedro',
        'tipo':'gato',
        'estado':'normal'
    }
    return render(req, 'perzomascota.html', ctx)