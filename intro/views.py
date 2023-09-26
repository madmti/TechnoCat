from django.shortcuts import render, redirect

def unMatch(req):
    ctx = {  }
    return render( req, 'nopage.html', ctx )

def menu(req, ssid=''):
    redirect('/msg/ssid_not_valid') if ssid == '' else ''
    ctx = {}
    return render( req, 'menu.html', ctx )

def landing(req, msg=''):
    ctx = { 'msg':msg if msg=='' else msg.replace('_', ' ') }
    return render( req, 'landing.html', ctx )

def panel(req, ssid=''):
    ctx = {}
    return render( req, 'panel.html', ctx )