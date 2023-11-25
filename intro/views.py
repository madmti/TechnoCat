from django.shortcuts import render, redirect
from api.views import validarSSID, getUserCR_CA_BySSID, getItems, procesarCompra, getUserDataBySSID, ItemlistFromDict
from api.models import LeaderBoard
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
CONFIGS = {
        0:{
            'back':'background-image: url(/static/img/back/base.jpg);',
            'element_0':'background-image: url(/static/img/back/trash_0.png);',
            'element_1':'background-image: url(/static/img/back/trash_1.png);',
            'element_2':'background-image: url(/static/img/back/trashcan_0.png); transform: translate(50px, 50px) rotateZ(90deg);',
            'element_3':'background-image: url(/static/img/back/trashcan_0.png);'
        },
        1:{
            'back':'background-image: url(/static/img/back/base.jpg);',
            'element_0':'background-image: url(/static/img/back/trash_0.png);',
            'element_1':'background-image: url(/static/img/back/trash_1.png);',
            'element_2':'visibility: hidden;',
            'element_3':'background-image: url(/static/img/back/trashcan_0.png);'
        },
        2:{
            'back':'background-image: url(/static/img/back/base.jpg);',
            'element_0':'visibility: hidden;',
            'element_1':'background-image: url(/static/img/back/trash_1.png);',
            'element_2':'visibility: hidden;',
            'element_3':'background-image: url(/static/img/back/trashcan_0.png);'
        },
        3:{
            'back':'background-image: url(/static/img/back/base.jpg);',
            'element_0':'visibility: hidden;',
            'element_1':'visibility: hidden;',
            'element_2':'visibility: hidden;',
            'element_3':'visibility: hidden;'
        },
        4:{
            'back':'background-image: url(/static/img/back/last.jpg);',
            'element_0':'visibility: hidden;',
            'element_1':'visibility: hidden;',
            'element_2':'visibility: hidden;',
            'element_3':'visibility: hidden;'
        },
        5:{
            'back':'background-image: url(/static/img/back/last.jpg);',
            'element_0':'visibility: hidden;',
            'element_1':'background-image: url(/static/img/back/flower.png);',
            'element_2':'visibility: hidden;',
            'element_3':'visibility: hidden;'
        },
        6:{
            'back':'background-image: url(/static/img/back/last.jpg);',
            'element_0':'visibility: hidden;',
            'element_1':'background-image: url(/static/img/back/flower.png); z-index: 1;',
            'element_2':'visibility: hidden;',
            'element_3':'background-image: url(/static/img/back/food.png); transform: translate(1rem, 5rem) scale(0.5); z-index: 0;',
        },
        7:{
            'back':'background-image: url(/static/img/back/last.jpg);',
            'element_0':'visibility: hidden;',
            'element_1':'background-image: url(/static/img/back/flower.png); z-index: 1;',
            'element_2':'background-image: url(/static/img/back/sand.png); transform: translate(1rem, 5rem) scale(0.5); z-index: 0;',
            'element_3':'background-image: url(/static/img/back/food.png); transform: translate(1rem, 5rem) scale(0.5); z-index: 0;',
        }
    }

# GENERAL
def landing(req, msg=''):
    ctx = { 'msg':msg if msg=='' else msg.replace('_', ' ') }
    return render( req, 'landing.html', ctx )

def menu(req, ssid):
    isValid, auth = validarSSID(ssid)
    if not isValid: return redirect('/msg/la_sesion_ya_no_es_valida')
    userInfo, petInfo, itemsInfo = getUserDataBySSID(ssid)
    if userInfo.NBA < len(CONFIGS):config = userInfo.NBA
    else: config = len(CONFIGS) - 1
    ctx = {
        'ssid':ssid,
        'PetInfo':petInfo,
        'petUrlImg':f'{TRAD[petInfo["estado"]]}/{TRAD[petInfo["tipo"]]}.png',
        'items':ItemlistFromDict(itemsInfo),
        'config':CONFIGS[config],
        'nba':userInfo.NBA
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
    _, PetData, _  = getUserDataBySSID(ssid)
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
    _, PetData, _  = getUserDataBySSID(ssid)
    ctx = {
        'ssid':ssid,
        'imgUrl':f'img/cat/{TRAD[PetData["estado"]]}/{TRAD[PetData["tipo"]]}.png',
        'records':LeaderBoard.get_Top()
        }
    return render(req, 'firstgame.html', ctx)