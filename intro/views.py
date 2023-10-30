from django.shortcuts import render, redirect
from api.views import validarSSID, getUserCR_CA_BySSID, getItems, procesarCompra

# GENERAL
def landing(req, msg=''):
    ctx = { 'msg':msg if msg=='' else msg.replace('_', ' ') }
    return render( req, 'landing.html', ctx )

def menu(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not isValid: return redirect('/msg/la_sesion_ya_no_es_valida')
    ctx = {
        'ssid':ssid
    }
    return render( req, 'menu.html', ctx )


def panel(req, ssid, msg=''):
    isValid, auth = validarSSID(ssid)
    if not (isValid and auth): return redirect('/msg/la_sesion_ya_no_es_valida')
    ctx = {'ssid':ssid, 'msg':msg.replace('_',' ')}
    return render( req, 'panel.html', ctx )


def PerzoMascota(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not isValid: return redirect('/msg/la_sesion_ya_no_es_valida')
    # TEST DATA
    ESTADOS = [
        'normal',
        'triste',
        'feliz',
    ]
    TIPOS = [
        'gato',
        'perro',
        'tortuga'
    ]
    # ---------
    ctx = {
        'petName':'pedro',
        'tipo':'gato',
        'estado':'normal',
        'ssid':ssid,
        'estadoList':ESTADOS,
        'tipoList':TIPOS,
    }
    return render(req, 'perzomascota.html', ctx)

def tienda(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not isValid: return redirect('/msg/la_sesion_ya_no_es_valida')

    if req.method == 'POST': procesarCompra(req.POST, ssid)

    Items = getItems()
    CR, CA = getUserCR_CA_BySSID(ssid)
    ctx = {
        'ssid':ssid,
        'CAitems':Items['CA'],
        'CRitems':Items['CR'],
        'CA':CA,
        'CR':CR
        }
    return render(req, 'tienda.html', ctx)

# JUEGOS
def selectGame(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not isValid: return redirect('/msg/la_sesion_ya_no_es_valida')
    ctx = {'ssid':ssid}

    return render(req, 'gameselect.html', ctx)

def firstGame(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not isValid: return redirect('/msg/la_sesion_ya_no_es_valida')
    ctx = {'ssid':ssid}
    return render(req, 'firstgame.html', ctx)