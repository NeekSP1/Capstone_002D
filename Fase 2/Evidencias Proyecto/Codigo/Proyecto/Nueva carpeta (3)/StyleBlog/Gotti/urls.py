from django.urls import path
from . import views

urlpatterns = [

    ##Principal
    path('', views.index, name='index'),
    path('contacto/', views.contacto, name='contacto'),
    path('iniciarCliente/', views.iniciarCliente, name='iniciarCliente'),
    path('iniciarColaborador/', views.iniciarColaborador, name='iniciarColaborador'),
    path('iniciarSesion/', views.iniciarSesion, name='iniciarSesion'),
    path('inicioCliente/', views.inicioCliente, name='inicioCliente'),
    path('inicioColaborador/', views.inicioColaborador, name='inicioColaborador'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('perfilCliente/', views.perfilCliente, name='perfilCliente'),
    path('perfilCliente/<int:id>/', views.perfilCliente, name='perfil_Cliente'),
    path('perfilColaborador/', views.perfilColaborador, name='perfilColaborador'),
    path('registrarse/', views.registrarse, name='registrarse'),
    ###barbero
    path('indexBarbero/', views.indexBarbero, name='indexBarbero'),
    path('carritobarbero/', views.carritobarbero, name='carritobarbero'),
    path('contactoact/', views.contactoact, name='contactoact'),
    path('contactobarbero/', views.contactobarbero, name='contactobarbero'),
    path('datosbarbero/', views.datosbarbero, name='datosbarbero'),
    path('horaeliminada/', views.horaeliminada, name='horaeliminada'),
    path('horareserva/', views.horareserva, name='horareserva'),
    path('productoact/', views.productoact, name='productoact'),
    path('productoact2/', views.productoact2, name='productoact2'),
    path('productoact3/', views.productoact3, name='productoact3'),
    path('productos/', views.productos, name='productos'),
    path('servicioact/', views.servicioact, name='servicioact'),
    path('servicioact2/', views.servicioact2, name='servicioact2'),
    path('servicioact3/', views.servicioact3, name='servicioact3'),
    path('servicios/', views.servicios, name='servicios'),
    path('verhora/', views.verhora, name='verhora'),

    ###cliente
    path('indexCliente/', views.indexCliente, name='indexCliente'),
    path('carritoCliente/', views.carritoCliente, name='carritoCliente'),
    path('contactoCliente/', views.contactoCliente, name='contactoCliente'),
    path('datosCliente/', views.datosCliente, name='datosCliente'),
    path('nosotrosCliente/', views.nosotrosCliente, name='nosotrosCliente'),
    path('productosCliente/', views.productosCliente, name='productosCliente'),
    path('servicioInfCliente/', views.servicioInfCliente, name='servicioInfCliente'),
    path('servicioInfCliente2/', views.servicioInfCliente2, name='servicioInfCliente2'),
    path('servicioInfCliente3/', views.servicioInfCliente3, name='servicioInfCliente3'),
    path('serviciosCliente/', views.serviciosCliente, name='serviciosCliente'),

]
