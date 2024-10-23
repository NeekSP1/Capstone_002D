from django.contrib import admin
from .models import Cliente, Barbero

# Registramos los modelos para que se muestren en el admin
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'contraseña', 'correoElectronico')
    search_fields = ('nombre', 'apellido', 'contraseña', 'correoElectronico')

@admin.register(Barbero)
class BarberoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'especialidad', 'horario', 'correoElectronico')
    search_fields = ('nombre', 'apellido', 'especialidad', 'correoElectronico')
