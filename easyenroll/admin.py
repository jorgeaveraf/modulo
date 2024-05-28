# easyenroll/admin.py

from django.contrib import admin
from .models import Alumno, Pago, PadresTutores, Inscripcion, AnexoAlumnos

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidoPaterno', 'apellidoMaterno', 'correoInstitucional')
    search_fields = ('nombre', 'apellidoPaterno', 'correoInstitucional')

class PagoAdmin(admin.ModelAdmin):
    list_display = ('idPago', 'recibo', 'descuento', 'idRecibo', 'monto', 'fechaPago', 'metodoPago')
    search_fields = ('idPago', 'recibo', 'idRecibo', 'metodoPago')
    list_filter = ('fechaPago', 'metodoPago')

class PadresTutoresAdmin(admin.ModelAdmin):
    list_display = ('nombrePadreTutor', 'curpTutor', 'telefono', 'emailPadreTutor')
    search_fields = ('nombrePadreTutor', 'curpTutor', 'emailPadreTutor')

class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'factura', 'tipoInscripcion', 'modalidadPago', 'idAlumno', 'idPago', 'idUsuario')
    search_fields = ('tipoInscripcion', 'modalidadPago')
    list_filter = ('factura', 'modalidadPago')

class AnexoAlumnosAdmin(admin.ModelAdmin):
    list_display = ('id', 'cartaBuenaConducta', 'certificadoPrimaria', 'curpAlumno', 'actaNacimiento', 'idAlumno')
    search_fields = ('id', 'curpAlumno')
    list_filter = ('cartaBuenaConducta', 'certificadoPrimaria', 'curpAlumno', 'actaNacimiento')

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Pago, PagoAdmin)
admin.site.register(PadresTutores, PadresTutoresAdmin)
admin.site.register(Inscripcion, InscripcionAdmin)
admin.site.register(AnexoAlumnos, AnexoAlumnosAdmin)
