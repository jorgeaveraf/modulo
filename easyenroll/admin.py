# easyenroll/admin.py

from django.contrib import admin
from .models import Alumno, Pago

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidoPaterno', 'apellidoMaterno', 'correoInstitucional')
    search_fields = ('nombre', 'apellidoPaterno', 'correoInstitucional')

#class PagoAdmin(admin.ModelAdmin):


admin.site.register(Alumno, AlumnoAdmin )
