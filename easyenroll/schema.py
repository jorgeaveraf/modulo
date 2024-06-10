from django.conf import settings
import graphene
from graphene_django import DjangoObjectType
from .models import Inscripcion, Pago, Alumno, PadresTutores, AnexoAlumnos
from users.schema import UserType
from django.contrib.auth import get_user_model
from django.db.models import Q
import re
from datetime import date, datetime
from graphql import GraphQLError

def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise GraphQLError("Correo institucional no tiene un formato válido")

def validate_curp(curp):
    if not re.match(r"^[A-Z0-9]{18}$", curp):
        raise GraphQLError("CURP no tiene un formato válido")
    
def validate_telefono(telefono):
    if not re.match(r"^\d{10}$", telefono):
        raise GraphQLError("El teléfono no tiene un formato válido")
    
def validate_url(url):
    if not re.match(r"^(http|https)://", url):
        raise GraphQLError("La URL no es válida")
    
def validate_modalidad_pago(modalidad_pago):
    if modalidad_pago not in ["12", "10"]:
        raise GraphQLError("Modalidad de pago no válida. Debe ser '12' o '10' meses")

def validate_tipo_inscripcion(tipo_inscripcion):
    if tipo_inscripcion not in ["I", "R"]:
        raise GraphQLError("Tipo de inscripción no válido. Debe ser 'Inscripcion' o 'Reinscripcion'")

def validate_descuento(descuento):
    if descuento < 0:
        raise GraphQLError("El descuento no puede ser negativo")
    if descuento > 100:
        raise GraphQLError("El descuento no puede ser mayor al 100%")

def validate_monto(monto):
    if monto <= 0:
        raise GraphQLError("El monto debe ser un valor positivo")

def validate_fecha_pago(fecha_pago):
    try:
        if isinstance(fecha_pago, str):
            fecha_pago = datetime.strptime(fecha_pago, '%Y-%m-%d').date()
        if fecha_pago > date.today():
            raise GraphQLError("La fecha de pago no puede ser una fecha futura")
    except ValueError:
        raise GraphQLError("El formato de la fecha debe ser YYYY-MM-DD")

def validate_metodo_pago(metodo_pago):
    valid_methods = ["E", "T", "Tr"]
    if metodo_pago not in valid_methods:
        raise GraphQLError("El método de pago no es válido")

def validate_lateralidad(lateralidad):
    valid_lateralidades = ["D", "I", "A"]
    if lateralidad not in valid_lateralidades:
        raise GraphQLError("La lateralidad no es válida")

class StudentType(DjangoObjectType):
    class Meta: 
        model = Alumno

class EnrollmentType(DjangoObjectType):
    class Meta:
        model = Inscripcion

class PaymentType(DjangoObjectType):
    class Meta:
        model = Pago

class TutorType(DjangoObjectType):
    class Meta:
        model = PadresTutores

class AnnexType(DjangoObjectType):
    class Meta:
        model = AnexoAlumnos

class Query(graphene.ObjectType):
    students = graphene.List(StudentType, search=graphene.String())
    enrollments = graphene.List(EnrollmentType, search=graphene.String(), tipo_inscripcion=graphene.String(), modalidad_pago=graphene.String(), id_alumno=graphene.String(), id_pago=graphene.Int(), id_usuario=graphene.String())
    payments = graphene.List(PaymentType)
    tutors = graphene.List(TutorType, search=graphene.String())
    annexes = graphene.List(AnnexType)

    def resolve_students(self, info, search=None):
        if search:
            filter = (
                Q(nombre__icontains=search)
            )
            return Alumno.objects.filter(filter)
        
        return Alumno.objects.all()
    
    def resolve_enrollments(self, info, tipo_inscripcion=None, modalidad_pago=None, id_alumno=None, id_pago=None, id_usuario=None):
        filter = Q()

        if tipo_inscripcion:
            filter &= Q(tipoInscripcion__icontains=tipo_inscripcion)
        
        if modalidad_pago:
            filter &= Q(modalidadPago__icontains=modalidad_pago)

        if id_alumno:
            filter &= Q(idAlumno__nombre__icontains=id_alumno)

        if id_pago:
            filter &= Q(idPago__idRecibo__icontains=id_pago)

        if id_usuario:
            filter &= Q(idUsuario__username__icontains=id_usuario)

        return Inscripcion.objects.filter(filter)


    def resolve_payments(self, info):
        return Pago.objects.all()

    def resolve_tutors(self, info, search=None):
        if search:
            filter = (
                Q(nombrePadreTutor__icontains=search)
            )
            return PadresTutores.objects.filter(filter)
        
        return PadresTutores.objects.all()

    def resolve_annexes(self, info):
        return AnexoAlumnos.objects.all()
    
class CreateAlumno(graphene.Mutation):
    id = graphene.Int()
    nombre = graphene.String()
    apellido_paterno = graphene.String()
    apellido_materno = graphene.String()
    correo_institucional = graphene.String()
    curp = graphene.String()
    sexo = graphene.String()
    escuela_procedencia = graphene.String()
    grado_grupo_asignado = graphene.String()

    class Arguments:
        nombre = graphene.String(required=True)
        apellido_paterno = graphene.String(required=True)
        apellido_materno = graphene.String(required=True)
        correo_institucional = graphene.String(required=True)
        curp = graphene.String(required=True)
        sexo = graphene.String(required=True)
        escuela_procedencia = graphene.String(required=True)
        grado_grupo_asignado = graphene.String(required=True)

    def mutate(self, info, nombre, apellido_paterno, apellido_materno, correo_institucional, curp, sexo, escuela_procedencia, grado_grupo_asignado):
        if len(nombre) > 100:
            raise GraphQLError("El nombre es demasiado largo")
        if len(apellido_paterno) > 100:
            raise GraphQLError("El apellido paterno es demasiado largo")
        if len(apellido_materno) > 100:
            raise GraphQLError("El apellido materno es demasiado largo")
        validate_email(correo_institucional)
        validate_curp(curp)
        if sexo not in ["M", "F"]:
            raise GraphQLError("El valor de sexo no es válido")

        student = Alumno(
            nombre=nombre,
            apellidoPaterno=apellido_paterno,
            apellidoMaterno=apellido_materno,
            correoInstitucional=correo_institucional,
            curp=curp,
            sexo=sexo,
            escuelaProcedencia=escuela_procedencia,
            gradoGrupoAsignado=grado_grupo_asignado
        )
        student.save()

        return CreateAlumno(
            id=student.id,
            nombre=student.nombre,
            apellido_paterno=student.apellidoPaterno,
            apellido_materno=student.apellidoMaterno,
            correo_institucional=student.correoInstitucional,
            curp=student.curp,
            sexo=student.sexo,
            escuela_procedencia=student.escuelaProcedencia,
            grado_grupo_asignado=student.gradoGrupoAsignado
        )
    
class ModifyAlumno(graphene.Mutation):
    id = graphene.Int()
    nombre = graphene.String()
    apellido_paterno = graphene.String()
    apellido_materno = graphene.String()
    correo_institucional = graphene.String()
    curp = graphene.String()
    sexo = graphene.String()
    escuela_procedencia = graphene.String()
    grado_grupo_asignado = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        nombre = graphene.String()
        apellido_paterno = graphene.String()
        apellido_materno = graphene.String()
        correo_institucional = graphene.String()
        curp = graphene.String()
        sexo = graphene.String()
        escuela_procedencia = graphene.String()
        grado_grupo_asignado = graphene.String()

    def mutate(self, info, id, nombre=None, apellido_paterno=None, apellido_materno=None, correo_institucional=None, curp=None, sexo=None, escuela_procedencia=None, grado_grupo_asignado=None):
        try:
            student = Alumno.objects.get(pk=id)
        except Alumno.DoesNotExist:
            raise GraphQLError("Alumno no encontrado")

        if nombre:
            if len(nombre) > 100:
                raise GraphQLError("El nombre es demasiado largo")
            student.nombre = nombre
        if apellido_paterno:
            if len(apellido_paterno) > 100:
                raise GraphQLError("El apellido paterno es demasiado largo")
            student.apellidoPaterno = apellido_paterno
        if apellido_materno:
            if len(apellido_materno) > 100:
                raise GraphQLError("El apellido materno es demasiado largo")
            student.apellidoMaterno = apellido_materno
        if correo_institucional:
            validate_email(correo_institucional)
            student.correoInstitucional = correo_institucional
        if curp:
            validate_curp(curp)
            student.curp = curp
        if sexo:
            if sexo not in ["M", "F"]:
                raise GraphQLError("El valor de sexo no es válido")
            student.sexo = sexo
        if escuela_procedencia:
            student.escuelaProcedencia = escuela_procedencia
        if grado_grupo_asignado:
            student.gradoGrupoAsignado = grado_grupo_asignado

        student.save()

        return ModifyAlumno(
            id=student.id,
            nombre=student.nombre,
            apellido_paterno=student.apellidoPaterno,
            apellido_materno=student.apellidoMaterno,
            correo_institucional=student.correoInstitucional,
            curp=student.curp,
            sexo=student.sexo,
            escuela_procedencia=student.escuelaProcedencia,
            grado_grupo_asignado=student.gradoGrupoAsignado
        )
    
class DeleteAlumno(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        try:
            student = Alumno.objects.get(pk=id)
        except Alumno.DoesNotExist:
            raise Exception("Alumno not found")
        
        student.delete()
        
        return DeleteAlumno(id=id)

class CreatePago(graphene.Mutation):
    id_pago = graphene.Int()
    recibo = graphene.String()
    descuento = graphene.Int()
    id_recibo = graphene.Int()
    monto = graphene.Float()
    fecha_pago = graphene.Date()
    metodo_pago = graphene.String()

    class Arguments:
        recibo = graphene.String(required=True)
        descuento = graphene.Int(required=False, default_value=0)
        id_recibo = graphene.Int(required=True)
        monto = graphene.Float(required=True)
        fecha_pago = graphene.Date(required=True)
        metodo_pago = graphene.String(required=True)

    def mutate(self, info, recibo, descuento, id_recibo, monto, fecha_pago, metodo_pago):
        validate_url(recibo)
        validate_descuento(descuento)
        validate_monto(monto)
        validate_fecha_pago(fecha_pago)
        validate_metodo_pago(metodo_pago)

        payment = Pago(recibo=recibo, descuento=descuento, idRecibo=id_recibo, monto=monto, fechaPago=fecha_pago, metodoPago=metodo_pago)
        payment.save()

        return CreatePago(
            id_pago=payment.idPago,
            recibo=payment.recibo,
            descuento=payment.descuento,
            id_recibo=payment.idRecibo,
            monto=payment.monto,
            fecha_pago=payment.fechaPago,
            metodo_pago=payment.metodoPago,
        )
    
class ModifyPago(graphene.Mutation):
    id_pago = graphene.Int()
    recibo = graphene.String()
    descuento = graphene.Int()
    id_recibo = graphene.Int()
    monto = graphene.Float()
    fecha_pago = graphene.Date()
    metodo_pago = graphene.String()

    class Arguments:
        id_pago = graphene.Int(required=True)
        recibo = graphene.String()
        descuento = graphene.Int()
        id_recibo = graphene.Int()
        monto = graphene.Float()
        fecha_pago = graphene.Date()
        metodo_pago = graphene.String()

    def mutate(self, info, id_pago, recibo=None, descuento=None, id_recibo=None, monto=None, fecha_pago=None, metodo_pago=None):
        try:
            payment = Pago.objects.get(pk=id_pago)
        except Pago.DoesNotExist:
            raise Exception("Payment not found")

        if recibo:
            validate_url(recibo)
            payment.recibo = recibo
        if descuento:
            validate_descuento(descuento)
            payment.descuento = descuento
        if id_recibo:
            payment.idRecibo = id_recibo
        if monto:
            validate_monto(monto)
            payment.monto = monto
        if fecha_pago:
            validate_fecha_pago(fecha_pago)
            payment.fechaPago = fecha_pago
        if metodo_pago:
            validate_metodo_pago(metodo_pago)
            payment.metodoPago = metodo_pago

        payment.save()
        
        return ModifyPago(
            id_pago=payment.idPago,
            recibo=payment.recibo,
            descuento=payment.descuento,
            id_recibo=payment.idRecibo,
            monto=payment.monto,
            fecha_pago=payment.fechaPago,
            metodo_pago=payment.metodoPago,
        )

class DeletePago(graphene.Mutation):
    id_pago = graphene.Int()

    class Arguments:
        id_pago = graphene.Int(required=True)

    def mutate(self, info, id_pago):
        try:
            payment = Pago.objects.get(pk=id_pago)
        except Pago.DoesNotExist:
            raise Exception("Payment not found")
        
        payment.delete()
        
        return DeletePago(id_pago=id_pago)

class CreatePadresTutores(graphene.Mutation):
    id = graphene.Int()
    nombre_padre_tutor = graphene.String()
    curp_tutor = graphene.String()
    scan_ine = graphene.String()
    telefono = graphene.String()
    scan_comprobante_domicilio = graphene.String()
    email_padre_tutor = graphene.String()
    alumno = graphene.Field(StudentType)

    class Arguments:
        nombre_padre_tutor = graphene.String(required=True)
        curp_tutor = graphene.String(required=True)
        scan_ine = graphene.String(required=True)
        telefono = graphene.String(required=True)
        scan_comprobante_domicilio = graphene.String(required=True)
        email_padre_tutor = graphene.String(required=True)
        alumno_id = graphene.Int(required=True)

    def mutate(self, info, nombre_padre_tutor, curp_tutor, scan_ine, telefono, scan_comprobante_domicilio, email_padre_tutor, alumno_id):
        if len(nombre_padre_tutor) > 100:
            raise GraphQLError("El nombre del padre/tutor es demasiado largo")
        
        validate_curp(curp_tutor)
        validate_url(scan_ine)
        validate_telefono(telefono)
        validate_url(scan_comprobante_domicilio)
        validate_email(email_padre_tutor)

        try:
            student = Alumno.objects.get(pk=alumno_id)
        except Alumno.DoesNotExist:
            raise GraphQLError("Alumno no encontrado")

        tutor = PadresTutores(
            nombrePadreTutor=nombre_padre_tutor,
            curpTutor=curp_tutor,
            scanIne=scan_ine,
            telefono=telefono,
            scanComprobanteDomicilio=scan_comprobante_domicilio,
            emailPadreTutor=email_padre_tutor,
            alumno=student
        )
        tutor.save()

        return CreatePadresTutores(
            id=tutor.id,
            nombre_padre_tutor=tutor.nombrePadreTutor,
            curp_tutor=tutor.curpTutor,
            scan_ine=tutor.scanIne,
            telefono=tutor.telefono,
            scan_comprobante_domicilio=tutor.scanComprobanteDomicilio,
            email_padre_tutor=tutor.emailPadreTutor,
            alumno=tutor.alumno,
        )

class ModifyPadresTutores(graphene.Mutation):
    id = graphene.Int()
    nombre_padre_tutor = graphene.String()
    curp_tutor = graphene.String()
    scan_ine = graphene.String()
    telefono = graphene.String()
    scan_comprobante_domicilio = graphene.String()
    email_padre_tutor = graphene.String()
    alumno = graphene.Field(StudentType)

    class Arguments:
        id = graphene.Int(required=True)
        nombre_padre_tutor = graphene.String()
        curp_tutor = graphene.String()
        scan_ine = graphene.String()
        telefono = graphene.String()
        scan_comprobante_domicilio = graphene.String()
        email_padre_tutor = graphene.String()
        alumno_id = graphene.Int()

    def mutate(self, info, id, nombre_padre_tutor=None, curp_tutor=None, scan_ine=None, telefono=None, scan_comprobante_domicilio=None, email_padre_tutor=None, alumno_id=None):
        try:
            tutor = PadresTutores.objects.get(pk=id)
        except PadresTutores.DoesNotExist:
            raise Exception("Tutor not found")

        if nombre_padre_tutor:
            if len(nombre_padre_tutor) > 100:
                raise GraphQLError("El nombre del padre/tutor es demasiado largo")
            tutor.nombrePadreTutor = nombre_padre_tutor
        
        if curp_tutor:
            validate_curp(curp_tutor)
            tutor.curpTutor = curp_tutor
        
        if telefono:
            validate_telefono(telefono)
            tutor.telefono = telefono
        
        if email_padre_tutor:
            validate_email(email_padre_tutor)
            tutor.emailPadreTutor = email_padre_tutor
        
        if scan_ine:
            validate_url(scan_ine)
            tutor.scanIne = scan_ine
        
        if scan_comprobante_domicilio:
            validate_url(scan_comprobante_domicilio)
            tutor.scanComprobanteDomicilio = scan_comprobante_domicilio
        
        if alumno_id:
            try:
                student = Alumno.objects.get(pk=alumno_id)
            except Alumno.DoesNotExist:
                raise GraphQLError("Alumno no encontrado")
            tutor.alumno = student

        tutor.save()
        
        return ModifyPadresTutores(
            id=tutor.id,
            nombre_padre_tutor=tutor.nombrePadreTutor,
            curp_tutor=tutor.curpTutor,
            scan_ine=tutor.scanIne,
            telefono=tutor.telefono,
            scan_comprobante_domicilio=tutor.scanComprobanteDomicilio,
            email_padre_tutor=tutor.emailPadreTutor,
            alumno=tutor.alumno,
        )

class DeletePadresTutores(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        try:
            tutor = PadresTutores.objects.get(pk=id)
        except PadresTutores.DoesNotExist:
            raise Exception("Tutor not found")
        
        tutor.delete()
        
        return DeletePadresTutores(id=id)

class CreateInscripcion(graphene.Mutation):
    id = graphene.Int()
    factura = graphene.Boolean()
    tipo_inscripcion = graphene.String()
    modalidad_pago = graphene.String()
    alumno = graphene.Field(lambda: StudentType)
    pago = graphene.Field(lambda: PaymentType)
    usuario = graphene.Field(lambda: UserType)

    class Arguments:
        factura = graphene.Boolean()
        tipo_inscripcion = graphene.String(required=True)
        modalidad_pago = graphene.String(required=True)
        id_alumno = graphene.Int(required=True)
        id_pago = graphene.Int(required=True)
        id_usuario = graphene.Int(required=True)

    def mutate(self, info, factura, tipo_inscripcion, modalidad_pago, id_alumno, id_pago, id_usuario):
        validate_modalidad_pago(modalidad_pago)
        validate_tipo_inscripcion(tipo_inscripcion)

        try:
            student = Alumno.objects.get(pk=id_alumno)
            payment = Pago.objects.get(pk=id_pago)
            user = get_user_model().objects.get(pk=id_usuario)
        except Alumno.DoesNotExist:
            raise GraphQLError("Alumno no encontrado")
        except Pago.DoesNotExist:
            raise GraphQLError("Pago no encontrado")
        except get_user_model().DoesNotExist:
            raise GraphQLError("Usuario no encontrado")

        enrollment = Inscripcion(
            factura=factura,
            tipoInscripcion=tipo_inscripcion,
            modalidadPago=modalidad_pago,
            idAlumno=student,
            idPago=payment,
            idUsuario=user
        )
        enrollment.save()

        return CreateInscripcion(
            id=enrollment.id,
            factura=enrollment.factura,
            tipo_inscripcion=enrollment.tipoInscripcion,
            modalidad_pago=enrollment.modalidadPago,
            alumno=enrollment.idAlumno,
            pago=enrollment.idPago,
            usuario=enrollment.idUsuario,
        )

class ModifyInscripcion(graphene.Mutation):
    id = graphene.Int()
    factura = graphene.Boolean()
    tipo_inscripcion = graphene.String()
    modalidad_pago = graphene.String()
    alumno = graphene.Field(lambda: StudentType)
    pago = graphene.Field(lambda: PaymentType)
    usuario = graphene.Field(lambda: UserType)

    class Arguments:
        id = graphene.Int(required=True)
        factura = graphene.Boolean()
        tipo_inscripcion = graphene.String()
        modalidad_pago = graphene.String()
        id_alumno = graphene.Int()
        id_pago = graphene.Int()
        id_usuario = graphene.Int()

    def mutate(self, info, id, factura=None, tipo_inscripcion=None, modalidad_pago=None, id_alumno=None, id_pago=None, id_usuario=None):
        try:
            enrollment = Inscripcion.objects.get(pk=id)
        except Inscripcion.DoesNotExist:
            raise Exception("Enrollment not found")

        if factura is not None:
            enrollment.factura = factura
        if tipo_inscripcion:
            validate_tipo_inscripcion(tipo_inscripcion)
            enrollment.tipoInscripcion = tipo_inscripcion
        if modalidad_pago:
            validate_modalidad_pago(modalidad_pago)
            enrollment.modalidadPago = modalidad_pago
        if id_alumno:
            try:
                student = Alumno.objects.get(pk=id_alumno)
                enrollment.idAlumno = student
            except Alumno.DoesNotExist:
                raise GraphQLError("Alumno no encontrado")
        if id_pago:
            try:
                payment = Pago.objects.get(pk=id_pago)
                enrollment.idPago = payment
            except Pago.DoesNotExist:
                raise GraphQLError("Pago no encontrado")
        if id_usuario:
            try:
                user = get_user_model().objects.get(pk=id_usuario)
                enrollment.idUsuario = user
            except get_user_model().DoesNotExist:
                raise GraphQLError("Usuario no encontrado")

        enrollment.save()
        
        return ModifyInscripcion(
            id=enrollment.id,
            factura=enrollment.factura,
            tipo_inscripcion=enrollment.tipoInscripcion,
            modalidad_pago=enrollment.modalidadPago,
            alumno=enrollment.idAlumno,
            pago=enrollment.idPago,
            usuario=enrollment.idUsuario,
        )

class DeleteInscripcion(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        try:
            enrollment = Inscripcion.objects.get(pk=id)
        except Inscripcion.DoesNotExist:
            raise Exception("Enrollment not found")
        
        enrollment.delete()
        
        return DeleteInscripcion(id=id)

class createAnexoAlumnos(graphene.Mutation):
    id = graphene.Int()
    carta_buena_conducta = graphene.Boolean()
    certificado_primaria = graphene.Boolean()
    curp_alumno = graphene.Boolean()
    acta_nacimiento = graphene.Boolean()
    observaciones = graphene.String()
    cda = graphene.String()
    autorizacion_irse_solo = graphene.Boolean()
    autorizacion_publicitaria = graphene.Boolean()
    atencion_psicologica = graphene.Boolean()
    padecimiento = graphene.String()
    uso_aparato_auditivo = graphene.Boolean()
    uso_de_lentes = graphene.Boolean()
    lateralidad = graphene.String()
    alumno = graphene.Field(lambda: StudentType)

    class Arguments:
        carta_buena_conducta = graphene.Boolean()
        certificado_primaria = graphene.Boolean()
        curp_alumno = graphene.Boolean()
        acta_nacimiento = graphene.Boolean()
        observaciones = graphene.String()
        cda = graphene.String()
        autorizacion_irse_solo = graphene.Boolean()
        autorizacion_publicitaria = graphene.Boolean()
        atencion_psicologica = graphene.Boolean()
        padecimiento = graphene.String()
        uso_aparato_auditivo = graphene.Boolean()
        uso_de_lentes = graphene.Boolean()
        lateralidad = graphene.String()
        id_alumno = graphene.Int(required=True)

    def mutate(self, info, carta_buena_conducta, certificado_primaria, curp_alumno, acta_nacimiento, observaciones, cda, autorizacion_irse_solo, autorizacion_publicitaria, atencion_psicologica, padecimiento, uso_aparato_auditivo, uso_de_lentes, lateralidad, id_alumno):
        try:
            student = Alumno.objects.get(pk=id_alumno)
        except Alumno.DoesNotExist:
            raise GraphQLError("Alumno no encontrado")
        

        annex = AnexoAlumnos(
            cartaBuenaConducta=carta_buena_conducta,
            certificadoPrimaria=certificado_primaria,
            curpAlumno=curp_alumno,
            actaNacimiento=acta_nacimiento,
            observaciones=observaciones,
            cda=cda,
            autorizacionIrseSolo=autorizacion_irse_solo,
            autorizacionPublicitaria=autorizacion_publicitaria,
            atencionPsicologica=atencion_psicologica,
            padecimiento=padecimiento,
            usoAparatoAuditivo=uso_aparato_auditivo,
            usoDeLentes=uso_de_lentes,
            lateralidad=lateralidad,
            idAlumno=student
        )
        annex.save()

        return createAnexoAlumnos(
            id=annex.id,
            carta_buena_conducta=annex.cartaBuenaConducta,
            certificado_primaria=annex.certificadoPrimaria,
            curp_alumno=annex.curpAlumno,
            acta_nacimiento=annex.actaNacimiento,
            observaciones=annex.observaciones,
            cda=annex.cda,
            autorizacion_irse_solo=annex.autorizacionIrseSolo,
            autorizacion_publicitaria=annex.autorizacionPublicitaria,
            atencion_psicologica=annex.atencionPsicologica,
            padecimiento=annex.padecimiento,
            uso_aparato_auditivo=annex.usoAparatoAuditivo,
            uso_de_lentes=annex.usoDeLentes,
            lateralidad=annex.lateralidad,
            alumno=annex.idAlumno,
        )

class ModifyAnexoAlumnos(graphene.Mutation):
    id = graphene.Int()
    carta_buena_conducta = graphene.Boolean()
    certificado_primaria = graphene.Boolean()
    curp_alumno = graphene.Boolean()
    acta_nacimiento = graphene.Boolean()
    observaciones = graphene.String()
    cda = graphene.String()
    autorizacion_irse_solo = graphene.Boolean()
    autorizacion_publicitaria = graphene.Boolean()
    atencion_psicologica = graphene.Boolean()
    padecimiento = graphene.String()
    uso_aparato_auditivo = graphene.Boolean()
    uso_de_lentes = graphene.Boolean()
    lateralidad = graphene.String()
    alumno = graphene.Field(lambda: StudentType)

    class Arguments:
        id = graphene.Int(required=True)
        carta_buena_conducta = graphene.Boolean()
        certificado_primaria = graphene.Boolean()
        curp_alumno = graphene.Boolean()
        acta_nacimiento = graphene.Boolean()
        observaciones = graphene.String()
        cda = graphene.String()
        autorizacion_irse_solo = graphene.Boolean()
        autorizacion_publicitaria = graphene.Boolean()
        atencion_psicologica = graphene.Boolean()
        padecimiento = graphene.String()
        uso_aparato_auditivo = graphene.Boolean()
        uso_de_lentes = graphene.Boolean()
        lateralidad = graphene.String()
        id_alumno = graphene.Int()

    def mutate(self, info, id, carta_buena_conducta=None, certificado_primaria=None, curp_alumno=None, acta_nacimiento=None, observaciones=None, cda=None, autorizacion_irse_solo=None, autorizacion_publicitaria=None, atencion_psicologica=None, padecimiento=None, uso_aparato_auditivo=None, uso_de_lentes=None, lateralidad=None, id_alumno=None):
        try:
            annex = AnexoAlumnos.objects.get(pk=id)
        except AnexoAlumnos.DoesNotExist:
            raise Exception("Annex not found")

        if carta_buena_conducta:
            annex.cartaBuenaConducta = carta_buena_conducta
        if certificado_primaria:
            annex.certificadoPrimaria = certificado_primaria
        if curp_alumno:
            annex.curpAlumno = curp_alumno
        if acta_nacimiento:
            annex.actaNacimiento = acta_nacimiento
        if observaciones:
            annex.observaciones = observaciones
        if cda:
            annex.cda = cda
        if autorizacion_irse_solo:
            annex.autorizacionIrseSolo = autorizacion_irse_solo
        if autorizacion_publicitaria:
            annex.autorizacionPublicitaria = autorizacion_publicitaria
        if atencion_psicologica:
            annex.atencionPsicologica = atencion_psicologica
        if padecimiento:
            annex.padecimiento = padecimiento
        if uso_aparato_auditivo:
            annex.usoAparatoAuditivo = uso_aparato_auditivo
        if uso_de_lentes:
            annex.usoDeLentes = uso_de_lentes
        if lateralidad:
            annex.lateralidad = lateralidad
        if id_alumno:
            student = Alumno.objects.get(pk=id_alumno)
            annex.idAlumno = student

        annex.save()

        return ModifyAnexoAlumnos(
            id=annex.id,
            carta_buena_conducta=annex.cartaBuenaConducta,
            certificado_primaria=annex.certificadoPrimaria,
            curp_alumno=annex.curpAlumno,
            acta_nacimiento=annex.actaNacimiento,
            observaciones=annex.observaciones,
            cda=annex.cda,
            autorizacion_irse_solo=annex.autorizacionIrseSolo,
            autorizacion_publicitaria=annex.autorizacionPublicitaria,
            atencion_psicologica=annex.atencionPsicologica,
            padecimiento=annex.padecimiento,
            uso_aparato_auditivo=annex.usoAparatoAuditivo,
            uso_de_lentes=annex.usoDeLentes,
            lateralidad=annex.lateralidad,
            alumno=annex.idAlumno,
        )
    
class DeleteAnexoAlumnos(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        try:
            annex = AnexoAlumnos.objects.get(pk=id)
        except AnexoAlumnos.DoesNotExist:
            raise Exception("Annex not found")
        
        annex.delete()
        
        return DeleteAnexoAlumnos(id=id)

class Mutation(graphene.ObjectType):
    create_student = CreateAlumno.Field()
    modify_student = ModifyAlumno.Field()
    delete_student = DeleteAlumno.Field()
    create_payment = CreatePago.Field()
    modify_payment = ModifyPago.Field()
    delete_payment = DeletePago.Field()
    create_tutor = CreatePadresTutores.Field()
    modify_tutor = ModifyPadresTutores.Field()
    delete_tutor = DeletePadresTutores.Field()
    create_enrollment = CreateInscripcion.Field()
    modify_enrollment = ModifyInscripcion.Field()
    delete_enrollment = DeleteInscripcion.Field()
    create_annex = createAnexoAlumnos.Field()
    modify_annex = ModifyAnexoAlumnos.Field()
    delete_annex = DeleteAnexoAlumnos.Field()
