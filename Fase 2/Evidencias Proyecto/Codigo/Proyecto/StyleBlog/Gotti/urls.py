from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contacto/', views.contacto, name='contacto'),
    path('iniciarCliente/', views.iniciarCliente, name='iniciarCliente'),
    path('iniciarColaborador/', views.iniciarColaborador, name='iniciarColaborador'),
    path('iniciarSesion/', views.iniciarSesion, name='iniciarSesion'),
    path('inicioCliente/', views.inicioCliente, name='inicioCliente'),
    path('inicioColaborador/', views.inicioColaborador, name='inicioColaborador'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('perfilCliente/', views.perfilCliente, name='perfilCliente'),
    path('perfilColaborador/', views.perfilColaborador, name='perfilColaborador'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('indexBarbero/', views.indexBarbero, name='indexBarbero'),
    path('indexCliente/', views.indexCliente, name='indexCliente'),
]
