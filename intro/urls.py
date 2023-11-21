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
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from api.views import *

#handler404 = 'api.views.unMatch'
#handler500 = 'api.views.th'

urlpatterns = [
    #Actions
    path('admin/', admin.site.urls),
    path('api/Log', validarForm),
    path('api/Reg', validarRegistro),
    path('api/update/<str:ssid>', UpdateUser),
    path('api/validateCREDS/', validarCred),
    path('api/updatePet/<str:ssid>', updatePet),
    path('api/recompensa/<str:ssid>', recompensas),

    #User Views
    path('', landing, name='landing'),
    path('msg/<str:msg>', landing),
    path('menu/<str:ssid>', menu),
    path('perzomascota/<str:ssid>', PerzoMascota),
    path('api/qr/<str:ssid>', QrCode),
    path('tienda/<str:ssid>', tienda),
    path('help/', help),
    path('about/', about),
        #-- juegos
        path('gameselect/<str:ssid>', selectGame),
        path('firstgame/<str:ssid>', firstGame),

    #Super Views
    path('panel/<str:ssid>', panel),
    path('panelscan/<str:ssid>', QrCodeScan),
    path('panelform/<str:ssid>', NoQrForm),
    path('scanmsg/<str:ssid>/<str:msg>', panel),
] + static(settings.STATIC_URL, document_root_=settings.STATIC_ROOT)
