from django.shortcuts import render, redirect

def menu(req):
    ctx = {}
    return render( req, 'menu.html', ctx )

def landing(req):
    ctx = {  }
    return render( req, 'landing.html', ctx )