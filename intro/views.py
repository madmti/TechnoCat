from django.shortcuts import render, redirect
from api.views import validarSSID, getUserCR_CA_BySSID, getItems, procesarCompra, getUserDataBySSID
# File Image Data
ESTADOS = [
    'negro',
    'mix_negro',
    'blanco_y_negro',
    'gris',
    'gris_persa',
    'mix_gris',
    'gris_tigre',
    'gris_y_blanco',
    'naranjo',
    'naranjo_tigre',
    'naranjo_y_blanco',
    'blanco'
]
TIPOS = [
    'pequeño',
    'normal',
    'XL'
]
TRAD = {
    'negro':'black',
    'mix_negro':'black-multi',
    'blanco_y_negro':'black-white',
    'gris':'gray',
    'gris_persa':'gray-faded',
    'mix_gris':'gray-multi',
    'gris_tigre':'gray-tiger',
    'gris_y_blanco':'gray-white',
    'naranjo':'orange',
    'naranjo_tigre':'orange-tiger',
    'naranjo_y_blanco':'orange-white',
    'blanco':'white',
    'XL':'xl',
    'pequeño':'small',
    'normal':'regular',
}

# GENERAL
def landing(req, msg=''):
    ctx = { 'msg':msg if msg=='' else msg.replace('_', ' ') }
    return render( req, 'landing.html', ctx )

def menu(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not isValid: return redirect('/msg/la_sesion_ya_no_es_valida')
    _, petInfo = getUserDataBySSID(ssid)
    ctx = {
        'ssid':ssid,
        'PetInfo':petInfo,
        'petUrlImg':f'{TRAD[petInfo["estado"]]}/{TRAD[petInfo["tipo"]]}.png'
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
    ( _, PetData ) = getUserDataBySSID(ssid)
    ctx = {
        'petName':PetData['name'],
        'tipo':PetData['tipo'],
        'estado':PetData['estado'],
        'ssid':ssid,
        'estadoList':ESTADOS,
        'tipoList':TIPOS,
        'imgUrl':f'cat/{TRAD[PetData["estado"]]}/{TRAD[PetData["tipo"]]}.png'
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

def help(req):
    origin = req.headers['Referer']
    ctx = {'origin':origin}
    return render(req, 'help.html', ctx)

def about(req):
    origin = req.headers['Referer']
    ctx = {'origin':origin}
    return render(req, 'about.html', ctx)

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