from django.shortcuts import render

def index(request):
    return render(request, 'Gotti/styleblog/index.html')

def contacto(request):
    return render(request, 'Gotti/styleblog/contacto.html')

def iniciarCliente(request):
    return render(request, 'Gotti/styleblog/iniciarCliente.html')

def iniciarColaborador(request):
    return render(request, 'Gotti/styleblog/iniciarColaborador.html')

def iniciarSesion(request):
    return render(request, 'Gotti/styleblog/iniciarSesion.html')

def inicioCliente(request):
    return render(request, 'Gotti/styleblog/inicioCliente.html')

def inicioColaborador(request):
    return render(request, 'Gotti/styleblog/inicioColaborador.html')

def nosotros(request):
    return render(request, 'Gotti/styleblog/nosotros.html')

def perfilCliente(request):
    return render(request, 'Gotti/styleblog/perfilCliente.html')

def perfilColaborador(request):
    return render(request, 'Gotti/styleblog/perfilColaborador.html')

def registrarse(request):
    return render(request, 'Gotti/styleblog/registrarse.html')

def indexBarbero(request):
    return render(request, 'Gotti/VistaBarbero/index.html')

def indexCliente(request):
    return render(request, 'Gotti/VistaCliente/index.html')

