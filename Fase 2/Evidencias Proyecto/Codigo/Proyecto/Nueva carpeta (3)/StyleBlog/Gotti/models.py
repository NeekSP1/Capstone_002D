from django.db import models

# Create your models here.
class DatosPersonales(models.Model):
    idDatoPersonal = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    correoElectronico = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellido} "

class Cliente(DatosPersonales):
    idCliente = models.AutoField(primary_key=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.telefono}"

class Barbero(DatosPersonales):
    idBarbero = models.AutoField(primary_key=True)
    especialidad = models.CharField(max_length=100)
    horario = models.DateField()

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.especialidad} {self.horario}"