from django.shortcuts import render, redirect





def landing(req):
    ctx = {  }
    return render( req, 'landing.html', ctx )