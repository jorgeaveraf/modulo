from django.db import models
from django.conf import settings

class Inscripcion(models.Model):
    id = models.AutoField(primary_key=True)
    factura = models.BooleanField(default=False)
    idUsuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idPago = models.ForeignKey('easyenroll.Pago', on_delete=models.CASCADE)
    idAlumno = models.ForeignKey('easyenroll.Alumno', on_delete=models.CASCADE)
    tipoInscripcion = models.CharField(max_length=10)
    modalidadPago = models.CharField(max_length=2)

class Pago(models.Model):
    idPago = models.AutoField(primary_key=True)
    recibo = models.URLField()
    descuento = models.IntegerField(default=0)
    idRecibo = models.IntegerField(null=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fechaPago = models.DateField()
    metodoPago = models.CharField(max_length=2)

class Alumno(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellidoPaterno = models.CharField(max_length=100)
    apellidoMaterno = models.CharField(max_length=100)
    correoInstitucional = models.EmailField()
    curp = models.CharField(max_length=18)
    sexo = models.CharField(max_length=1)
    escuelaProcedencia = models.CharField(max_length=100)
    gradoGrupoAsignado = models.CharField(max_length=2)


class PadresTutores(models.Model):
    id = models.AutoField(primary_key=True)
    nombrePadreTutor = models.CharField(max_length=100)
    curpTutor = models.CharField(max_length=18)
    scanIne = models.URLField()
    telefono = models.CharField(max_length=20)
    scanComprobanteDomicilio = models.URLField()
    emailPadreTutor = models.EmailField()
    alumno = models.ForeignKey('easyenroll.Alumno', on_delete=models.CASCADE)


class AnexoAlumnos(models.Model):
    id = models.AutoField(primary_key=True)
    cartaBuenaConducta = models.BooleanField(default=False)
    certificadoPrimaria = models.BooleanField(default=False)
    curpAlumno = models.BooleanField(default=False)
    actaNacimiento = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)
    cda = models.URLField(blank=True)
    autorizacionIrseSolo = models.BooleanField(default=False)
    autorizacionPublicitaria = models.BooleanField(default=False)
    atencionPsicologica = models.BooleanField(default=False)
    padecimiento = models.TextField(blank=True)
    usoAparatoAuditivo = models.BooleanField(default=False)
    usoDeLentes = models.BooleanField(default=False)
    lateralidad = models.CharField(max_length=1)
    idAlumno = models.ForeignKey('easyenroll.Alumno', on_delete=models.CASCADE)