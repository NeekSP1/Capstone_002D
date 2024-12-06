import re
import random
import Gotti.auth as log_user
import Gotti.auth_barbero as log_barbero
from .forms import ProductoForm,ServicioForm, ContactInfoForm
from Gotti.models import Cliente, Barbero, Producto, Servicio, ContactInfo, Carrito, BloqueHorario, CarritoProducto, BarberoPendiente
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Q
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from datetime import datetime, date
import json
from django.conf import settings
from datetime import datetime, date, timedelta
from django.db import transaction





def index(request):
    if log_user.is_authenticated(request):
        return redirect('inicioCliente')
    return render(request, 'Gotti/styleblog/index.html')

def contacto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        comentario = request.POST.get("comentario")

        # Crear el mensaje para el correo
        subject = f"Consulta de {nombre} {apellido}"
        message = f"Nombre: {nombre} {apellido}\nCorreo: {correo}\nComentario: {comentario}"
        from_email = correo  # Usamos el correo del usuario como remitente

        try:
            # Enviar el correo
            send_mail(subject, message, from_email, ['fbarrosquezada@gmail.com'])
            messages.success(request, "Tu mensaje ha sido enviado con éxito.")
        except Exception as e:
            messages.error(request, f"Hubo un error al enviar el correo: {e}")

    return render(request, 'Gotti/styleblog/contacto.html')

def contactoColaboradors(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        comentario = request.POST.get("comentario")

        # Crear el mensaje para el correo
        subject = f"Consulta de {nombre} {apellido}"
        message = f"Nombre: {nombre} {apellido}\nCorreo: {correo}\nComentario: {comentario}"
        from_email = correo  # Usamos el correo del usuario como remitente

        try:
            # Enviar el correo
            send_mail(subject, message, from_email, ['fbarrosquezada@gmail.com'])
            messages.success(request, "Tu mensaje ha sido enviado con éxito.")
        except Exception as e:
            messages.error(request, f"Hubo un error al enviar el correo: {e}")

    return render(request, 'Gotti/styleblog/contactoColaborador.html')

def contactoClientes(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        comentario = request.POST.get("comentario")

        # Crear el mensaje para el correo
        subject = f"Consulta de {nombre} {apellido}"
        message = f"Nombre: {nombre} {apellido}\nCorreo: {correo}\nComentario: {comentario}"
        from_email = correo  # Usamos el correo del usuario como remitente

        try:
            # Enviar el correo
            send_mail(subject, message, from_email, ['fbarrosquezada@gmail.com'])
            messages.success(request, "Tu mensaje ha sido enviado con éxito.")
        except Exception as e:
            messages.error(request, f"Hubo un error al enviar el correo: {e}")

    return render(request, 'Gotti/styleblog/contactoCliente.html')

def iniciarCliente(request):
    if request.method == 'POST':
        correo = request.POST.get('email')
        contraseña = request.POST.get('password')
        cliente =  log_user.authenticate_user(correo, contraseña)
        if cliente == None:

            messages.error(request, "El correo o la contraseña son incorrectos.")
            return redirect('iniciarCliente')
        log_user.login_user(request,cliente)

        return redirect('inicioCliente')
    if log_user.is_authenticated(request):
        return redirect('inicioCliente')

    return render(request, 'Gotti/styleblog/iniciarCliente.html')

def iniciarColaborador(request):
    # Si el usuario ya está autenticado, redirige a inicioColaborador
    if log_barbero.is2_authenticated(request):
        return redirect('inicioColaborador')

    # Si el usuario no está autenticado, permite que se muestre el formulario
    if request.method == 'POST':
        correo = request.POST.get('email')
        contraseña = request.POST.get('password')
        barbero = log_barbero.authenticate_barbero(correo, contraseña)

        # Si la autenticación falla, muestra un mensaje de error
        if barbero is None:
            messages.error(request, "El correo o la contraseña son incorrectos.")
            return redirect('iniciarColaborador')

        # Si la autenticación tiene éxito, inicia sesión y redirige a inicioColaborador
        log_barbero.login_barbero(request, barbero)
        return redirect('inicioColaborador')

    # Si el método no es POST (por ejemplo, es GET), muestra el formulario de inicio de sesión
    return render(request, 'Gotti/styleblog/iniciarColaborador.html')

def registrarse_como(request):
    return render(request, 'Gotti/styleblog/registrarse_como.html')

def iniciarSesion(request):
    if log_user.is_authenticated(request):
        return redirect('inicioCliente')
    if log_barbero.is2_authenticated(request):
        return redirect('inicioColaborador')
    return render(request, 'Gotti/styleblog/iniciarSesion.html')

def inicioCliente(request):
    return render(request, 'Gotti/styleblog/inicioCliente.html')

def inicioColaborador(request):
    return render(request, 'Gotti/styleblog/inicioColaborador.html')

def nosotros(request):
    return render(request, 'Gotti/styleblog/nosotros.html')

def nosotrosColaboradors(request):
    return render(request, 'Gotti/styleblog/nosotrosColaborador.html')

def nosotrosClientes(request):
    return render(request, 'Gotti/styleblog/nosotrosCliente.html')

@log_user.custom_login_required
def perfilCliente(request):
    cliente = Cliente.objects.get(idCliente=request.session.get('user_id'))  # Obtener el cliente logueado

    if request.method == 'POST':
        # Obtener y actualizar los datos del formulario
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.correoElectronico = request.POST.get('email')

        # Verificar si se ha ingresado una nueva contraseña y si coincide con la confirmación
        nueva_contraseña = request.POST.get('password')
        confirmar_contraseña = request.POST.get('confirm_password')

        if nueva_contraseña and nueva_contraseña == confirmar_contraseña:
            cliente.contraseña = make_password(nueva_contraseña)  # Encriptar nueva contraseña
        elif nueva_contraseña != confirmar_contraseña:
            messages.error(request, "Las contraseñas no coinciden.", extra_tags='perfilCliente')  # Mostrar mensaje de error si no coinciden
            return redirect('perfilCliente')  # Redirigir de nuevo a la página para corregir

        cliente.save()  # Guardar los cambios en la base de datos
        messages.success(request, "Datos actualizados correctamente.", extra_tags='perfilCliente')
        return redirect('perfilCliente')  # Redirigir a la misma página para ver los cambios

    # Enviar los datos actuales al template
    return render(request, 'Gotti/styleblog/perfilCliente.html', {'cliente': cliente})

@log_barbero.custom2_login_required
def perfilColaborador(request):
    barbero = Barbero.objects.get(idBarbero=request.session.get('user_id'))

    if request.method == 'POST':
        barbero.nombre = request.POST.get('nombre')
        barbero.apellido = request.POST.get('apellido')
        barbero.correoElectronico = request.POST.get('email')

        nueva_contraseña = request.POST.get('password')
        confirmar_contraseña = request.POST.get('confirm_password')

        # Verificar si las contraseñas coinciden y si son válidas
        if nueva_contraseña and nueva_contraseña == confirmar_contraseña:
            # Validar que la contraseña tenga al menos una mayúscula
            if not re.search(r'[A-Z]', nueva_contraseña):
                messages.error(request, "La contraseña debe contener al menos una letra mayúscula.", extra_tags='perfilColaborador')
                return redirect('perfilColaborador')
            barbero.contraseña = make_password(nueva_contraseña)
        elif nueva_contraseña != confirmar_contraseña:
            messages.error(request, "Las contraseñas no coinciden.", extra_tags='perfilColaborador')
            return redirect('perfilColaborador')

        barbero.save()
        messages.success(request, "Datos actualizados correctamente.")
        return redirect('perfilColaborador')

    return render(request, 'Gotti/styleblog/perfilColaborador.html', {'barbero': barbero})

def registrarse(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('email')
        contraseña = request.POST.get('password')
        confirmar_contraseña = request.POST.get('confirm_password')

        # Validación del formato del correo
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, correo):
            messages.error(request, "El correo ingresado no tiene un formato válido.")
            return redirect('registrarse')

        # Validación de las contraseñas
        if contraseña != confirmar_contraseña:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('registrarse')
        if len(contraseña) < 8:
            messages.error(request, "La contraseña debe tener al menos 8 caracteres.")
            return redirect('registrarse')
        if not re.search(r'[A-Z]', contraseña):
            messages.error(request, "La contraseña debe contener al menos una letra mayúscula.")
            return redirect('registrarse')

        try:
            # Verificar si el correo ya existe
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

            # Pasar el mensaje de éxito al iniciar sesión
            messages.success(request, "Cuenta creada exitosamente. Por favor, inicia sesión.")
            return redirect('iniciarSesion')  # Redirigir a la página de inicio de sesión

        except IntegrityError:
            # Manejo de error por correo duplicado (caso extremo)
            messages.error(request, "Este correo ya está registrado.")
            return redirect('registrarse')

    return render(request, 'Gotti/styleblog/registrarse.html')

def aprobacion_confirmada(request):
    return render(request, 'Gotti/styleblog/aprobacion_confirmada.html')

def recuperar_contraseña(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Verificar si el correo está registrado en Cliente o Barbero
        try:
            usuario = Cliente.objects.get(correoElectronico=email)
        except Cliente.DoesNotExist:
            try:
                usuario = Barbero.objects.get(correoElectronico=email)
            except Barbero.DoesNotExist:
                messages.error(request, 'El correo ingresado no está registrado.')
                return redirect('recuperar_contraseña')

        # Generar un código de verificación aleatorio
        codigo = random.randint(100000, 999999)

        # Guardar el código en la sesión para validación posterior
        request.session['codigo_verificacion'] = codigo
        request.session['email_recuperacion'] = email

        # Enviar el correo con el código
        send_mail(
            'Recuperación de contraseña - Style Blog',
            f'Hemos recibido una solicitud para modificar tu contraseña. Ingresa el siguiente código para continuar: {codigo}',
            'tu_correo@dominio.com',  # Reemplaza con tu correo real
            [email],
            fail_silently=False,
        )

        messages.success(request, 'Se ha enviado un código de verificación a tu correo electrónico.')
        return redirect('verificar_codigo')

    return render(request, 'Gotti/styleblog/recuperar_contraseña.html')

def verificar_codigo(request):
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo')
        codigo_correcto = request.session.get('codigo_verificacion')

        if str(codigo_ingresado) == str(codigo_correcto):
            # Código correcto, permitir restablecimiento de contraseña
            messages.success(request, 'Código verificado correctamente. Ahora puedes restablecer tu contraseña.')
            return redirect('restablecer_contraseña')
        else:
            # Código incorrecto
            messages.error(request, 'El código ingresado es incorrecto.')
            return redirect('verificar_codigo')

    return render(request, 'Gotti/styleblog/verificar_codigo.html')

def restablecer_contraseña(request):
    if request.method == 'POST':
        nueva_contraseña = request.POST.get('new_password')
        confirmar_contraseña = request.POST.get('confirm_password')
        email = request.session.get('email_recuperacion')

        # Verificar que el correo esté en sesión
        if not email:
            messages.error(request, "No se ha encontrado el correo para restablecer la contraseña. Intenta nuevamente.")
            return redirect('recuperar_contraseña')

        # Verificar si las contraseñas coinciden
        if nueva_contraseña != confirmar_contraseña:
            messages.error(request, 'Las contraseñas no coinciden. Inténtalo de nuevo.')
            return redirect('restablecer_contraseña')

        # Buscar en Cliente y Barbero
        usuario = None
        es_cliente = False

        try:
            usuario = Cliente.objects.get(correoElectronico=email)
            es_cliente = True
        except Cliente.DoesNotExist:
            try:
                usuario = Barbero.objects.get(correoElectronico=email)
            except Barbero.DoesNotExist:
                messages.error(request, "No se encontró un usuario registrado con el correo proporcionado.")
                return redirect('recuperar_contraseña')

        # Actualizar la contraseña
        usuario.contraseña = make_password(nueva_contraseña)
        usuario.save()

        # Eliminar datos de la sesión
        del request.session['codigo_verificacion']
        del request.session['email_recuperacion']

        # Mensaje de éxito
        tipo_usuario = "Cliente" if es_cliente else "Barbero"
        messages.success(request, f"Contraseña restablecida exitosamente para el {tipo_usuario}.")
        return redirect('confirmacion_recuperacion')

    return render(request, 'Gotti/styleblog/restablecer_contraseña.html')


def confirmacion_recuperacion(request):
    return render(request, 'Gotti/styleblog/confirmacion_recuperacion.html')


## Barbero
def indexbarbero(request):
    return render(request, 'Gotti/VistaBarbero/indexbarbero.html')

def carritobarbero(request):
    # Obtiene carritos que están reservados o cancelados
    carritos = Carrito.objects.filter(
        Q(reservado=True) | Q(cancelado=True)
    ).select_related('cliente').prefetch_related('carrito_productos__producto')

    pedidos_por_confirmar = []
    pedidos_confirmados = []

    for carrito in carritos:
        carrito_productos = carrito.carrito_productos.all()
        total_pedido = 0

        productos = []
        for cp in carrito_productos:
            subtotal = cp.producto.precio * cp.cantidad
            total_pedido += subtotal
            productos.append({
                'nombre': cp.producto.nombreProducto,
                'cantidad': cp.cantidad,
                'precio_unitario': cp.producto.precio,
                'subtotal': subtotal,
            })

        pedido = {
            'cliente': carrito.cliente,
            'productos': productos,
            'total': total_pedido,
            'carrito_id': carrito.idCarrito,
            'confirmado': carrito.confirmado,
            'cancelado': carrito.cancelado,
        }

        if carrito.confirmado:
            pedidos_confirmados.append(pedido)
        else:
            pedidos_por_confirmar.append(pedido)

    return render(request, 'Gotti/VistaBarbero/carritobarbero.html', {
        'pedidos_por_confirmar': pedidos_por_confirmar,
        'pedidos_confirmados': pedidos_confirmados,
    })




def confirmar_pedido(request):
    if request.method == 'POST':
        # Obtener y decodificar la lista de IDs
        seleccionados_json = request.POST.get('seleccionados', '[]')
        seleccionados = json.loads(seleccionados_json)

        # Iterar sobre los IDs seleccionados
        for carrito_id in seleccionados:
            carrito = get_object_or_404(Carrito, idCarrito=int(carrito_id))
            carrito.confirmado = True
            carrito.save()

            # Preparar detalles del pedido
            productos = carrito.carrito_productos.all()
            productos_texto = "\n".join(
                [f"- {cp.producto.nombreProducto}: {cp.cantidad} unidad(es) x ${cp.producto.precio} = ${cp.cantidad * cp.producto.precio}" for cp in productos]
            )
            total_pedido = sum(cp.cantidad * cp.producto.precio for cp in productos)

            cliente_email = carrito.cliente.correoElectronico
            subject = "Pedido confirmado - Gotti Barbería"
            message = (
                f"Hola {carrito.cliente.nombre},\n\n"
                "Tu pedido ha sido confirmado. Gracias por tu preferencia.\n\n"
                f"{productos_texto}\n\n"
                f"Total: ${total_pedido}\n\n"
                "Saludos,\nGotti Barbería"
            )

            # Enviar correo al cliente
            try:
                send_mail(
                    subject, message, 'fbarrosquezada@gmail.com', [cliente_email], fail_silently=False
                )
                messages.success(request, f"El pedido de {carrito.cliente.nombre} ha sido confirmado.")
            except Exception as e:
                messages.error(request, f"Error al enviar correo para {carrito.cliente.nombre}: {e}")

    return redirect('carritobarbero')




def cancelar_pedido(request):
    if request.method == 'POST':
        seleccionados_json = request.POST.get('seleccionados', '[]')
        seleccionados = json.loads(seleccionados_json)

        for carrito_id in seleccionados:
            carrito = get_object_or_404(Carrito, idCarrito=int(carrito_id))

            # Verificar si el pedido ya está confirmado. Si es así, no se puede cancelar
            if carrito.confirmado:
                messages.error(request, f"El pedido ya ha sido confirmado y no se puede cancelar.")
                continue

            carrito_productos = CarritoProducto.objects.filter(carrito=carrito)

            # Restaurar el stock sin duplicar
            for cp in carrito_productos:
                producto = cp.producto
                producto.stock += cp.cantidad  # Solo devolvemos el stock reservado
                producto.save()

            carrito_productos.delete()

            # Cambiar el estado del carrito a no reservado y permitir modificaciones
            carrito.reservado = False
            carrito.confirmado = False
            carrito.save()

            # Preparar el correo
            cliente_email = carrito.cliente.correoElectronico
            subject = "Pedido cancelado - Gotti Barbería"
            message = (
                f"Hola {carrito.cliente.nombre},\n\n"
                "Lamentablemente, tu pedido en Gotti Barbería ha sido cancelado.\n\n"
                "Si tienes alguna consulta, no dudes en ponerte en contacto con nosotros\n\n"
                "al WhatsApp +56987654321.\n\n"
                "Saludos,\nGotti Barbería"
            )

            try:
                send_mail(
                    subject,
                    message,
                    'fbarrosquezada@gmail.com',  # Remitente
                    [cliente_email],  # Destinatario
                    fail_silently=False,
                )
                messages.success(request, f"El pedido ha sido cancelado y se ha enviado un correo a {carrito.cliente.nombre}.")
            except Exception as e:
                messages.error(request, f"Hubo un error al enviar el correo: {e}")

    return redirect('carritobarbero')

def limpiar_pedidos_confirmados(request):
    if request.method == 'POST':
        carrito_ids = request.POST.getlist('seleccionados')  # Obtener los carritos seleccionados
        for carrito_id in carrito_ids:
            carrito = get_object_or_404(Carrito, idCarrito=carrito_id)
            if carrito.confirmado:
                carrito.confirmado = False  # Limpiar los pedidos confirmados
                carrito.save()
        messages.success(request, "Los pedidos confirmados han sido limpiados.")
        return redirect('carritobarbero')

def contactoact(request):
    contact_info = ContactInfo.objects.get(pk=1)  # Obtener la primera entrada
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=contact_info)
        if form.is_valid():
            form.save()  # Guardar la información
            print(form)
            return redirect('contactobarbero')  # Redirigir después de guardar
        else:
            print('error')
    else:
        form = ContactInfoForm(instance=contact_info)  # Población del formulario
    return render(request, 'Gotti/VistaBarbero/contactoact.html',{'form': form, 'contact_info': contact_info})


def contactobarbero(request):
    contact_info = ContactInfo.objects.get(pk=1)  # Obtener la primera entrada
    return render(request, 'Gotti/VistaBarbero/contactobarbero.html',{'contact_info': contact_info})

def serviciosbarbero(request):
    servicios = Servicio.objects.all()  # Obtiene todos los servicios
    return render(request, 'Gotti/VistaBarbero/serviciosbarbero.html', {'servicios': servicios})

def verhora(request):
    return render(request, 'Gotti/VistaBarbero/verhora.html')

def crear_horarios(request, idServicio):
    servicio = get_object_or_404(Servicio, idServicio=idServicio)  # Obtener el servicio correspondiente

    # Lista de horarios disponibles
    horas = [
        "--:--","08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
        "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
        "14:00", "14:30", "15:00", "15:30", "16:00", "16:30",
        "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00"
    ]

    ahora = datetime.now()  # Hora actual del sistema
    hora_actual = datetime.strptime(ahora.strftime("%H:%M"), "%H:%M")  # Hora actual en formato datetime
    hora_maxima = datetime.strptime("20:00", "%H:%M")  # Límite máximo del día
    fecha_actual = ahora.strftime("%Y-%m-%d")  # Fecha actual como cadena

    if request.method == 'POST':
        horarioinicio = request.POST.get('horarioinicio')
        horariofin = request.POST.get('horariofin')
        duracion_bloque = request.POST.get('duracion_bloque')  # Nueva duración en minutos
        fecha = request.POST.get('fecha')

        # Validación de campos vacíos
        if not horarioinicio or not horariofin or not fecha or not duracion_bloque:
            messages.error(request, "Por favor, completa todos los campos.", extra_tags="crear_horario")
            return redirect('crear_horarios', idServicio=idServicio)

        # Convertir horarios a objetos datetime para comparaciones
        horarioinicio_dt = datetime.strptime(horarioinicio, "%H:%M")
        horariofin_dt = datetime.strptime(horariofin, "%H:%M")
        try:
            duracion_bloque = int(duracion_bloque)
        except ValueError:
            messages.error(request, "La duración del bloque debe ser un número válido.", extra_tags="crear_horario")
            return redirect('crear_horarios', idServicio=idServicio)

        # Validación: No permitir agendar si ya pasó la hora máxima en el día actual
        if fecha == fecha_actual and hora_actual > hora_maxima:
            messages.error(request, "Ya no puedes agendar horas para hoy, ha pasado la hora límite (20:00).", extra_tags="crear_horario")
            return redirect('crear_horarios', idServicio=idServicio)

        # Validación: No permitir horas de inicio que ya pasaron en el día actual
        if fecha == fecha_actual and horarioinicio_dt < hora_actual:
            messages.error(request, "No puedes seleccionar una hora de inicio que ya ha pasado.", extra_tags="crear_horario")
            return redirect('crear_horarios', idServicio=idServicio)

        # Validación del rango de horarios
        if horarioinicio_dt >= horariofin_dt:
            messages.error(request, "El horario de fin debe ser mayor al horario de inicio.", extra_tags="crear_horario")
            return redirect('crear_horarios', idServicio=idServicio)

        # Crear múltiples bloques dentro del rango seleccionado
        bloques_creados = 0
        while horarioinicio_dt + timedelta(minutes=duracion_bloque) <= horariofin_dt:
            horario_fin_bloque = horarioinicio_dt + timedelta(minutes=duracion_bloque)

            # Verificar si el bloque termina dentro del rango horario seleccionado
            if horario_fin_bloque > horariofin_dt:
                break  # Detener el bucle si el bloque excede el horario de fin

            # Verificación de duplicado
            if not BloqueHorario.objects.filter(
                servicio=servicio,
                fecha=fecha,
                horarioinicio=horarioinicio_dt.strftime("%H:%M"),
                horariofin=horario_fin_bloque.strftime("%H:%M"),
            ).exists():
                # Crear un nuevo bloque de horario
                BloqueHorario.objects.create(
                    servicio=servicio,
                    horarioinicio=horarioinicio_dt.strftime("%H:%M"),
                    horariofin=horario_fin_bloque.strftime("%H:%M"),
                    fecha=fecha
                )
                bloques_creados += 1

            # Avanzar al siguiente bloque
            horarioinicio_dt = horario_fin_bloque

        if bloques_creados > 0:
            messages.success(request, f"Se han creado {bloques_creados} bloques de horario.", extra_tags="crear_horario")
        else:
            messages.warning(request, "No se crearon nuevos bloques, ya existen horarios similares.", extra_tags="crear_horario")

        # Redirige para que la página se recargue y se vea el mensaje
        return redirect('crear_horarios', idServicio=idServicio)

    # Renderizar el formulario
    return render(request, 'Gotti/VistaBarbero/crear_horarios.html', {
        'servicio': servicio,
        'horas': horas
    })

def ver_todos_horarios(request, idServicio):
    servicio = get_object_or_404(Servicio, idServicio=idServicio)
    horarios = BloqueHorario.objects.filter(servicio=servicio).order_by('fecha', 'horarioinicio')

    # Dividir en futuros y pasados
    horarios_futuros = horarios.filter(fecha__gte=date.today())
    horarios_pasados = horarios.filter(fecha__lt=date.today())

    # Paginación para horarios futuros
    paginator_futuros = Paginator(horarios_futuros, 10)
    page_number_futuros = request.GET.get('page_futuros')
    page_obj_futuros = paginator_futuros.get_page(page_number_futuros)

    # Paginación para horarios pasados
    paginator_pasados = Paginator(horarios_pasados, 10)
    page_number_pasados = request.GET.get('page_pasados')
    page_obj_pasados = paginator_pasados.get_page(page_number_pasados)

    if request.method == 'POST':
        # Obtener los IDs de los horarios seleccionados desde los checkboxes
        horarios_futuros_seleccionados = request.POST.getlist('horarios_futuros')
        horarios_pasados_seleccionados = request.POST.getlist('horarios_pasados')

        if horarios_futuros_seleccionados:
            # Eliminar los horarios futuros seleccionados
            BloqueHorario.objects.filter(idbloque__in=horarios_futuros_seleccionados).delete()
            messages.success(request, "Horarios futuros eliminados exitosamente.")

        if horarios_pasados_seleccionados:
            # Eliminar los horarios pasados seleccionados
            BloqueHorario.objects.filter(idbloque__in=horarios_pasados_seleccionados).delete()
            messages.success(request, "Horarios pasados eliminados exitosamente.")

        if not horarios_futuros_seleccionados and not horarios_pasados_seleccionados:
            messages.error(request, "No se seleccionaron horarios para eliminar.")

    return render(request, 'Gotti/VistaBarbero/ver_todos_horarios.html', {
        'servicio': servicio,
        'page_obj_futuros': page_obj_futuros,
        'page_obj_pasados': page_obj_pasados,
    })

def eliminar_horario(request, idbloque):
    horario = get_object_or_404(BloqueHorario, idbloque=idbloque)
    horario.delete()
    messages.success(request, "El bloque de horario ha sido eliminado exitosamente.")
    return redirect(request.META.get('HTTP_REFERER', 'ver_todos_horarios'))

def horas_reservadas(request):
    hoy = timezone.now().date()

    # Cargar los datos directamente de la base de datos
    horas_hoy = BloqueHorario.objects.filter(fecha=hoy).order_by('horarioinicio')
    horas_pasadas = BloqueHorario.objects.filter(fecha__lt=hoy).order_by('-fecha', 'horarioinicio')
    horas_otros_dias = BloqueHorario.objects.filter(fecha__gt=hoy).order_by('fecha', 'horarioinicio')

    # Paginación
    paginador_hoy = Paginator(horas_hoy, 10)
    paginador_pasadas = Paginator(horas_pasadas, 10)
    paginador_futuras = Paginator(horas_otros_dias, 10)

    horas_hoy_page = paginador_hoy.get_page(request.GET.get('page_hoy'))
    horas_pasadas_page = paginador_pasadas.get_page(request.GET.get('page_pasadas'))
    horas_otros_dias_page = paginador_futuras.get_page(request.GET.get('page_futuras'))

    context = {
        'horas_hoy': horas_hoy_page,
        'horas_pasadas': horas_pasadas_page,
        'horas_otros_dias': horas_otros_dias_page,
        'hoy': hoy
    }
    return render(request, 'Gotti/VistaBarbero/horas_reservadas.html', context)

def aceptar_hora(request, bloque_id):
    bloque = get_object_or_404(BloqueHorario, idbloque=bloque_id)

    if bloque.disponibilidad == "OCUPADO" and bloque.cliente:
        bloque.disponibilidad = "CONFIRMADO"
        bloque.save()

        # Enviar correo al cliente
        cliente = bloque.cliente
        subject = "¡Tu hora fue reservada! - Gotti Barbería"
        message = (
            f"Hola {cliente.nombre},\n\n"
            "¡Tu solicitud fue recibida con éxito!\n\n"
            f"Tu hora es para el día {bloque.fecha.strftime('%d/%m/%Y')}, desde las {bloque.horarioinicio.strftime('%H:%M')} "
            f"hasta las {bloque.horariofin.strftime('%H:%M')}.\n\n"
            "¡Recuerda llegar 10 minutos antes!\n\n"
            "En caso de cualquier problema contactate con nosotros al WhatsApp +56987654321.\n\n"
            "Gracias por confiar en Gotti Barbería.\n\n"
            "Saludos,\nGotti Barbería"
        )

        try:
            send_mail(
                subject,
                message,
                'fbarrosquezada@gmail.com',  # Remitente
                [cliente.correoElectronico],  # Destinatario
                fail_silently=False,
            )
            messages.success(request, f"Hora confirmada y correo enviado a {cliente.nombre}.")
        except Exception as e:
            messages.error(request, f"Hubo un error al enviar el correo: {e}")
    else:
        messages.error(request, "No se puede confirmar esta hora.")  # Mensaje de error si no es OCUPADO

    return redirect('horas_reservadas')

def cancelar_hora(request, bloque_id):
    bloque = get_object_or_404(BloqueHorario, idbloque=bloque_id)

    if bloque.disponibilidad in ["OCUPADO", "CONFIRMADO"]:
        cliente = bloque.cliente
        bloque.disponibilidad = "DISPONIBLE"
        bloque.cliente = None
        bloque.save()

        if cliente:
            subject = "Hora Cancelada - Gotti Barbería"
            message = (
                f"Hola {cliente.nombre},\n\n"
                "Lo lamentamos, pero el barbero tuvo que cancelar tu hora.\n\n"
                "Esperamos puedas volver a agendar otra. Disculpa las molestias.\n\n"
                "Si tienes algún reclamo o duda, contactate con nosotros en nuestro WhatsApp al +56987654321.\n\n"
                "Saludos,\nBarbería Gotti"
            )

            try:
                send_mail(
                    subject,
                    message,
                    'fbarrosquezada@gmail.com',  # Remitente
                    [cliente.correoElectronico],  # Destinatario
                    fail_silently=False,
                )
                messages.success(request, f"Hora cancelada y correo enviado a {cliente.nombre}.")
            except Exception as e:
                messages.error(request, f"Hubo un error al enviar el correo: {e}")
    else:
        messages.error(request, "Esta hora no puede ser cancelada.")  # Mensaje de error si no es OCUPADO o CONFIRMADO

    return redirect('horas_reservadas')

## CLiente
@log_user.custom_login_required
def indexCliente(request):
    return render(request, 'Gotti/VistaCliente/index.html')

def carritoCliente(request):
    carrito_id = request.session.get('carrito_id')
    carrito = Carrito.objects.filter(idCarrito=carrito_id).first()

    if not carrito:
        context = {
            'productos': [],
            'total': 0,
            'reservado': False,
        }
        messages.info(request, "No hay productos en el carrito.")
        return render(request, 'Gotti/VistaCliente/carrito.html', context)

    carrito_productos = CarritoProducto.objects.filter(carrito=carrito).select_related('producto')
    total = 0
    productos = []
    for cp in carrito_productos:
        subtotal = cp.producto.precio * cp.cantidad
        total += subtotal
        productos.append({
            'idProducto': cp.producto.idProducto,
            'nombreProducto': cp.producto.nombreProducto,
            'precio': cp.producto.precio,
            'cantidad': cp.cantidad,
            'subtotal': subtotal,
        })

    context = {
        'productos': productos,
        'total': total,
        'reservado': carrito.reservado,
    }
    return render(request, 'Gotti/VistaCliente/carrito.html', context)


def contactoCliente(request):
    contact_info = ContactInfo.objects.get(pk=1)  # Obtener la primera entrada
    return render(request, 'Gotti/VistaCliente/contacto.html',{'contact_info': contact_info})

def nosotrosCliente(request):
    return render(request, 'Gotti/VistaCliente/nosotros.html')

def productosCliente(request):
    productos = Producto.objects.all()  # Obtiene todos los productos desde la base de datos
    return render(request, 'Gotti/VistaCliente/productos.html', {'productos': productos})

def servicio(request):
    servicios = Servicio.objects.all()  # Obtén todos los servicios creados por el barbero
    return render(request, 'Gotti/VistaCliente/servicio.html', {'servicios': servicios})

def horarios_disponibles_cliente(request, idServicio):
    # Obtener el servicio específico
    servicio = get_object_or_404(Servicio, idServicio=idServicio)

    # Filtrar bloques de horario disponibles por fecha >= hoy y disponibilidad
    hoy = timezone.now().date()
    bloques_disponibles = BloqueHorario.objects.filter(
        servicio=servicio,
        fecha__gte=hoy,
        disponibilidad="DISPONIBLE"
    ).order_by('fecha', 'horarioinicio')  # Ordenar por fecha y hora de inicio

    context = {
        'servicio': servicio,
        'bloques_disponibles': bloques_disponibles
    }
    return render(request, 'Gotti/VistaCliente/horarios_disponibles_cliente.html', context)

def agendar_horario(request, bloque_id):
    bloque = get_object_or_404(BloqueHorario, idbloque=bloque_id)

    # Verificar si el usuario está autenticado
    if log_user.is_authenticated(request):
        cliente = Cliente.objects.get(idCliente=request.session.get('user_id'))

        # Verificar si el bloque está disponible
        if bloque.disponibilidad == "DISPONIBLE":
            bloque.disponibilidad = "OCUPADO"
            bloque.cliente = cliente
            bloque.save()

            # Refrescar el estado del bloque para obtener el valor actualizado
            bloque.refresh_from_db()

            return render(request, 'Gotti/VistaCliente/agendar_confirmacion.html', {'bloque': bloque})

    return redirect('horarios_disponibles_cliente', idServicio=bloque.servicio.idServicio)

def cerrar_sesion(request):
    log_user.logout_user(request)  # Cierra la sesión del cliente
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('iniciarSesion')  # Redirige a la página de inicio de sesión

# Cerrar sesión para Colaborador (Barbero)
def cerrar_sesion2(request):
    log_barbero.logout_barbero(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('iniciarSesion')




# Vistas protegidas para Barberos
@log_barbero.custom2_login_required
def productosbarbero(request):
    productos = Producto.objects.all()
    return render(request, 'Gotti/VistaBarbero/productosbarbero.html', {'productos': productos})

@log_barbero.custom2_login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto agregado correctamente.")
            return redirect('productosbarbero')
    else:
        form = ProductoForm()
    return render(request, 'Gotti/VistaBarbero/agregar_producto.html', {'form': form})

@log_barbero.custom2_login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, idProducto=id)

    if request.method == 'POST':
        # Formulario dinámico generado con la instancia del producto
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('productosbarbero')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'Gotti/VistaBarbero/editar_producto.html', {'form': form, 'producto': producto})


@log_barbero.custom2_login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, idProducto=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('productosbarbero')
    return render(request, 'Gotti/VistaBarbero/eliminar_producto.html', {'producto': producto})

@log_barbero.custom2_login_required
def agregar_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio agregado correctamente.")
            return redirect('serviciosbarbero')
    else:
        form = ServicioForm()
    return render(request, 'Gotti/VistaBarbero/agregar_servicio.html', {'form': form})

@log_barbero.custom2_login_required
def editar_servicio(request, id):
    servicio = get_object_or_404(Servicio, idServicio=id)
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio actualizado correctamente.")
            return redirect('serviciosbarbero')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'Gotti/VistaBarbero/editar_servicio.html', {'form': form, 'servicio': servicio})

@log_barbero.custom2_login_required
def eliminar_servicio(request, id):
    servicio = get_object_or_404(Servicio, idServicio=id)
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, "Servicio eliminado correctamente.")
        return redirect('serviciosbarbero')
    return render(request, 'Gotti/VistaBarbero/eliminar_servicio.html', {'servicio': servicio})

def agregar_al_carrito(request, id):
    # Obtener el producto y el cliente logueado
    producto = get_object_or_404(Producto, idProducto=id)
    cliente = Cliente.objects.get(idCliente=request.session.get('user_id'))  # Identifica al cliente

    # Verificar si se envió la cantidad desde el formulario
    cantidad = int(request.POST.get('cantidad', 1))

    # Verificar si hay suficiente stock disponible
    if producto.stock < cantidad:
        messages.error(request, f"El producto '{producto.nombreProducto}' no tiene suficiente stock disponible.")
        return redirect('productosCliente')

    # Manejo de carritos del cliente
    try:
        with transaction.atomic():  # Garantizar consistencia en la base de datos
            # Filtrar carritos no reservados para el cliente
            carritos = Carrito.objects.filter(cliente=cliente, reservado=False)

            if carritos.exists():
                if carritos.count() > 1:
                    # Si hay múltiples carritos no reservados, limpia los extra
                    carritos.exclude(idCarrito=carritos.first().idCarrito).delete()

                # Usa el carrito restante
                carrito = carritos.first()
            else:
                # Si no hay carritos no reservados, crea uno
                carrito = Carrito.objects.create(cliente=cliente, reservado=False)

    except Exception as e:
        messages.error(request, f"Error al gestionar carritos: {e}")
        return redirect('productosCliente')

    # Verificar si el producto ya está en el carrito
    carrito_producto, created = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)

    if not created:  # Si ya existe, incrementa la cantidad
        if producto.stock >= carrito_producto.cantidad + cantidad:
            carrito_producto.cantidad += cantidad
            carrito_producto.save()
            producto.stock -= cantidad  # Reducir el stock
            producto.save()
        else:
            messages.error(request, f"El producto '{producto.nombreProducto}' no tiene suficiente stock disponible.")
            return redirect('productosCliente')
    else:
        # Nuevo producto en el carrito
        carrito_producto.cantidad = cantidad
        carrito_producto.save()
        producto.stock -= cantidad  # Reducir el stock
        producto.save()

    request.session['carrito_id'] = carrito.idCarrito  # Guarda el carrito en la sesión
    messages.success(request, f"{cantidad} unidad(es) de '{producto.nombreProducto}' han sido añadidas al carrito.")
    return redirect('productosCliente')


def eliminar_del_carrito(request, id):
    carrito_id = request.session.get('carrito_id')
    carrito = Carrito.objects.filter(idCarrito=carrito_id).first()
    if carrito:
        carrito_producto = get_object_or_404(CarritoProducto, carrito=carrito, producto__idProducto=id)
        if carrito_producto.cantidad > 1:
            carrito_producto.cantidad -= 1
            carrito_producto.save()
        else:
            carrito_producto.delete()
        producto = carrito_producto.producto
        producto.stock += 1
        producto.save()
        messages.success(request, f"Se ha eliminado una unidad de '{producto.nombreProducto}' del carrito.")

    return redirect('carritoCliente')



def reservar_carrito(request):
    carrito_id = request.session.get('carrito_id')
    carrito = Carrito.objects.filter(idCarrito=carrito_id).first()

    if carrito:
        carrito.reservado = True  # Marca el carrito como reservado
        carrito.save()
        messages.success(request, "Carrito reservado exitosamente.")

    return redirect('carritoCliente')  # Redirige al carrito del cliente después de reservar




def registro_barbero(request):
    if request.method == 'POST':
        # Recopilar datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correoElectronico = request.POST.get('correoElectronico')
        contraseña = request.POST.get('contraseña')
        confirmar_contraseña = request.POST.get('confirm_password')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        especialidad = request.POST.get('especialidad')
        horario = request.POST.get('horario')

        # Validación del formato del correo
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, correoElectronico):
            messages.error(request, "El correo ingresado no tiene un formato válido.")
            return redirect('registro_barbero')

        # Validación del número de teléfono (exactamente 9 dígitos)
        if not re.fullmatch(r'\d{9}', telefono):
            messages.error(request, "El número de teléfono debe ser válido")
            return redirect('registro_barbero')

        # Validación de la contraseña
        if contraseña != confirmar_contraseña:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('registro_barbero')
        if len(contraseña) < 8:
            messages.error(request, "La contraseña debe tener al menos 8 caracteres.")
            return redirect('registro_barbero')
        if not re.search(r'[A-Z]', contraseña):
            messages.error(request, "La contraseña debe contener al menos una letra mayúscula.")
            return redirect('registro_barbero')

        # Verificar si ya existe un registro con el mismo correo
        if BarberoPendiente.objects.filter(correoElectronico=correoElectronico).exists() or \
           Barbero.objects.filter(correoElectronico=correoElectronico).exists() or \
           Cliente.objects.filter(correoElectronico=correoElectronico).exists():
            messages.error(request, "El correo ya está registrado.")
            return redirect('registro_barbero')

        # Crear un nuevo registro en BarberoPendiente
        BarberoPendiente.objects.create(
            nombre=nombre,
            apellido=apellido,
            contraseña=make_password(contraseña),
            direccion=direccion,
            correoElectronico=correoElectronico,
            telefono=telefono,
            especialidad=especialidad,
            horario=horario,
        )
        # Crear el mensaje para el correo
        subject = "Nuevo Barbero Registrado para Aprobación"
        message = (
            f"Un nuevo barbero se ha registrado y está pendiente de aprobación.\n\n"
            f"Nombre: {nombre} {apellido}\n"
            f"Correo: {correoElectronico}\n"
            f"Teléfono: {telefono}\n"
            f"Especialidad: {especialidad}\n"
            f"Dirección: {direccion}\n"
        )
        from_email = "fbarrosquezada@gmail.com"
        admin_email = "matiagodoygutierrez@gmail.com"

        try:
            # Enviar el correo al administrador
            send_mail(subject, message, from_email, [admin_email])
            messages.success(request, "Tu registro se ha completado con éxito. El administrador será notificado.")
        except Exception as e:
            messages.error(request, f"Hubo un error al enviar el correo al administrador: {e}")



        return redirect('aprobacion_confirmada')

    return render(request, 'Gotti/styleblog/registro_barbero.html')

# Solo usuarios con permisos de superusuario pueden acceder
@login_required
def aprobar_barberos(request):
    if request.method == 'POST':
        barberos_seleccionados = request.POST.getlist('barberos')
        for barbero_id in barberos_seleccionados:
            try:
                # Buscar el BarberoPendiente correspondiente
                barbero_pendiente = BarberoPendiente.objects.get(idBarberoPendiente=barbero_id)

                # Crear un nuevo registro en el modelo Barbero
                Barbero.objects.create(
                    nombre=barbero_pendiente.nombre,
                    apellido=barbero_pendiente.apellido,
                    contraseña=barbero_pendiente.contraseña,  # Ya encriptada
                    direccion=barbero_pendiente.direccion,
                    correoElectronico=barbero_pendiente.correoElectronico,
                    telefono=barbero_pendiente.telefono,
                    especialidad=barbero_pendiente.especialidad,
                    horario=barbero_pendiente.horario,
                )

                # Marcar como aprobado
                barbero_pendiente.aprobado = True
                barbero_pendiente.save()

            except Exception as e:
                print(f"Error al aprobar barbero {barbero_id}: {e}")

        return redirect('aprobar_barberos')

    # Mostrar lista de barberos pendientes
    barberos_pendientes = BarberoPendiente.objects.filter(aprobado=False)
    return render(request, 'Gotti/styleblog/aprobar_barberos.html', {'barberos_pendientes': barberos_pendientes})

def actualizar_cantidad(request, id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        carrito_id = request.session.get('carrito_id')
        carrito = Carrito.objects.filter(idCarrito=carrito_id).first()
        if carrito:
            carrito_producto = get_object_or_404(CarritoProducto, carrito=carrito, producto__idProducto=id)
            if cantidad > 0 and cantidad <= carrito_producto.producto.stock:
                diferencia = cantidad - carrito_producto.cantidad
                carrito_producto.cantidad = cantidad
                carrito_producto.save()

                # Actualizar el stock del producto
                producto = carrito_producto.producto
                producto.stock -= diferencia
                producto.save()

                messages.success(request, f"La cantidad de '{producto.nombreProducto}' ha sido actualizada.")
            else:
                messages.error(request, "Cantidad no válida o insuficiente stock.")

    return redirect('carritoCliente')

