from django.shortcuts import render, redirect
from .models import User

# Create your views here.
def validarForm(req):
    if req.method == 'POST':
        form = User(req.POST)
        print(form)
    
    return redirect('/menu')