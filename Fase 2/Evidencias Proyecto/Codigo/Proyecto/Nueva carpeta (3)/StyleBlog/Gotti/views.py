from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from Gotti.models import Cliente


def index(request):
    return render(request, 'Gotti/styleblog/index.html')

def contacto(request):
    return render(request, 'Gotti/styleblog/contacto.html')

def iniciarCliente(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        contraseña = request.POST.get('password')

        # Verificar si el correo electrónico existe
        try:
            cliente = Cliente.objects.get(correoElectronico=email)
            
            # Verificar la contraseña encriptada
            if check_password(contraseña, cliente.contraseña):
                # Aquí puedes iniciar la sesión del cliente si usas sesiones de Django
                messages.success(request, "Inicio de sesión exitoso.")
                return redirect('inicioCliente')  # Redirigir a la página deseada tras el inicio de sesión
            else:
                # Contraseña incorrecta
                messages.error(request, "Contraseña incorrecta.")
                return redirect('iniciarCliente')  # Volver a la página de inicio de sesión

        except Cliente.DoesNotExist:
            # El correo electrónico no existe en la base de datos
            messages.error(request, "El correo electrónico no está registrado.")
            return redirect('iniciarCliente')  # Volver a la página de inicio de sesión
    
    # Si es un GET o no es válido, solo mostrar el formulario
    return render(request, 'Gotti/styleblog/inicioCliente.html')

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
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('email')
        contraseña = request.POST.get('password')

        # Verificar si el correo ya existe en la base de datos
        if Cliente.objects.filter(correoElectronico=correo).exists():
            messages.error(request, "Este correo ya está registrado.")
            return redirect('registrarse')  # Redirigir a la página de registro

        # Crear un nuevo cliente
        cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            correoElectronico=correo,
            contraseña=make_password(contraseña),  # Encriptar la contraseña
        )
        cliente.save()
        messages.success(request, "Registro exitoso. Puedes iniciar sesión ahora.")
        return redirect('iniciarSesion')  # Redirigir a la página de inicio de sesión
    return render(request, 'Gotti/styleblog/registrarse.html')


def indexBarbero(request):
    return render(request, 'Gotti/VistaBarbero/index.html')

def carritobarbero(request):
    return render(request, 'Gotti/VistaCliente/carritobarbero.html')

def contactoact(request):
    return render(request, 'Gotti/VistaCliente/contactoact.html')

def contactobarbero(request):
    return render(request, 'Gotti/VistaCliente/contactobarbero.html')

def datosbarbero(request):
    return render(request, 'Gotti/VistaCliente/datosbarbero.html')

def horaeliminada(request):
    return render(request, 'Gotti/VistaCliente/horaeliminada.html')

def horareserva(request):
    return render(request, 'Gotti/VistaCliente/horareserva.html')

def productoact(request):
    return render(request, 'Gotti/VistaCliente/productoact.html')

def productoact2(request):
    return render(request, 'Gotti/VistaCliente/productoact2.html')

def productoact3(request):
    return render(request, 'Gotti/VistaCliente/productoact3.html')

def productos(request):
    return render(request, 'Gotti/VistaCliente/productos.html')

def servicioact(request):
    return render(request, 'Gotti/VistaCliente/servicioact.html')

def servicioact2(request):
    return render(request, 'Gotti/VistaCliente/servicioact2.html')

def servicioact3(request):
    return render(request, 'Gotti/VistaCliente/servicioact3.html')

def servicios(request):
    return render(request, 'Gotti/VistaCliente/servicios.html')

def verhora(request):
    return render(request, 'Gotti/VistaCliente/verhora.html')

def indexCliente(request):
    return render(request, 'Gotti/VistaCliente/index.html')

def carritoCliente(request):
    return render(request, 'Gotti/VistaCliente/carrito.html')

def contactoCliente(request):
    return render(request, 'Gotti/VistaCliente/contacto.html')

def datosCliente(request):
    return render(request, 'Gotti/VistaCliente/datos.html')

def nosotrosCliente(request):
    return render(request, 'Gotti/VistaCliente/nosotros.html')

def productosCliente(request):
    return render(request, 'Gotti/VistaCliente/productos.html')

def servicioInfCliente(request):
    return render(request, 'Gotti/VistaCliente/servicioinf.html')

def servicioInfCliente2(request):
    return render(request, 'Gotti/VistaCliente/servicioinf2.html')

def servicioInfCliente3(request):
    return render(request, 'Gotti/VistaCliente/servicioinf3.html')

def serviciosCliente(request):
    return render(request, 'Gotti/VistaCliente/servicios.html')


