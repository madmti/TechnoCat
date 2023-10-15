"""intro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from api.views import *

#handler404 = 'api.views.unMatch'
#handler500 = 'api.views.th'

urlpatterns = [
    #Actions
    path('admin/', admin.site.urls),
    path('api/Log', validarForm),
    path('api/Reg', validarRegistro),
    path('api/update/<slug:data>', UpdateUser),
    path('api/validateCREDS/', validarCred),

    #User Views
    path('', landing, name='landing'),
    path('msg/<str:msg>', landing),
    path('menu/<str:ssid>', menu),
    path('perzomascota/<str:ssid>', PerzoMascota),
    path('api/qr/<str:id>', QrCode),

    #Super Views
    path('panel/<str:ssid>', panel),
    path('panelscan/<str:ssid>', QrCodeScan),
]
