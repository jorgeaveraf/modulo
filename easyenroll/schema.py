from django.conf import settings
import graphene
from graphene_django import DjangoObjectType
from .models import Inscripcion, Pago, Alumno, PadresTutores, AnexoAlumnos
from users.schema import UserType
from django.contrib.auth import get_user_model

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
    students = graphene.List(StudentType)
    enrollments = graphene.List(EnrollmentType)
    payments = graphene.List(PaymentType)
    tutors = graphene.List(TutorType)
    annexes = graphene.List(AnnexType)

    def resolve_students(self, info):
        return Alumno.objects.all()

    def resolve_enrollments(self, info):
        return Inscripcion.objects.all()

    def resolve_payments(self, info):
        return Pago.objects.all()

    def resolve_tutors(self, info):
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
        nombre = graphene.String()
        apellido_paterno = graphene.String()
        apellido_materno = graphene.String()
        correo_institucional = graphene.String()
        curp = graphene.String()
        sexo = graphene.String()
        escuela_procedencia = graphene.String()
        grado_grupo_asignado = graphene.String()

    def mutate(self, info, nombre, apellido_paterno, apellido_materno, correo_institucional, curp, sexo, escuela_procedencia, grado_grupo_asignado):
        student = Alumno(nombre=nombre, apellidoPaterno=apellido_paterno, apellidoMaterno=apellido_materno, correoInstitucional=correo_institucional, curp=curp, sexo=sexo, escuelaProcedencia=escuela_procedencia, gradoGrupoAsignado=grado_grupo_asignado)
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
            grado_grupo_asignado=student.gradoGrupoAsignado,
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
            raise Exception("Alumno not found")

        if nombre:
            student.nombre = nombre
        if apellido_paterno:
            student.apellidoPaterno = apellido_paterno
        if apellido_materno:
            student.apellidoMaterno = apellido_materno
        if correo_institucional:
            student.correoInstitucional = correo_institucional
        if curp:
            student.curp = curp
        if sexo:
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
            grado_grupo_asignado=student.gradoGrupoAsignado,
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
        recibo = graphene.String()
        descuento = graphene.Int()
        id_recibo = graphene.Int()
        monto = graphene.Float()
        fecha_pago = graphene.Date()
        metodo_pago = graphene.String()

    def mutate(self, info, recibo, descuento, id_recibo, monto, fecha_pago, metodo_pago):
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
            payment.recibo = recibo
        if descuento:
            payment.descuento = descuento
        if id_recibo:
            payment.idRecibo = id_recibo
        if monto:
            payment.monto = monto
        if fecha_pago:
            payment.fechaPago = fecha_pago
        if metodo_pago:
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
        nombre_padre_tutor = graphene.String()
        curp_tutor = graphene.String()
        scan_ine = graphene.String()
        telefono = graphene.String()
        scan_comprobante_domicilio = graphene.String()
        email_padre_tutor = graphene.String()
        alumno_id = graphene.Int()

    def mutate(self, info, nombre_padre_tutor, curp_tutor, scan_ine, telefono, scan_comprobante_domicilio, email_padre_tutor, alumno_id):
        student = Alumno.objects.get(pk=alumno_id)
        tutor = PadresTutores(nombrePadreTutor=nombre_padre_tutor, curpTutor=curp_tutor, scanIne=scan_ine, telefono=telefono, scanComprobanteDomicilio=scan_comprobante_domicilio, emailPadreTutor=email_padre_tutor, alumno=student)
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
            tutor.nombrePadreTutor = nombre_padre_tutor
        if curp_tutor:
            tutor.curpTutor = curp_tutor
        if scan_ine:
            tutor.scanIne = scan_ine
        if telefono:
            tutor.telefono = telefono
        if scan_comprobante_domicilio:
            tutor.scanComprobanteDomicilio = scan_comprobante_domicilio
        if email_padre_tutor:
            tutor.emailPadreTutor = email_padre_tutor
        if alumno_id:
            student = Alumno.objects.get(pk=alumno_id)
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
        tipo_inscripcion = graphene.String()
        modalidad_pago = graphene.String()
        id_alumno = graphene.Int()
        id_pago = graphene.Int()
        id_usuario = graphene.Int()

    def mutate(self, info, factura, tipo_inscripcion, modalidad_pago, id_alumno, id_pago, id_usuario):
        student = Alumno.objects.get(pk=id_alumno)
        payment = Pago.objects.get(pk=id_pago)
        user = get_user_model().objects.get(pk=id_usuario)
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

        if factura:
            enrollment.factura = factura
        if tipo_inscripcion:
            enrollment.tipoInscripcion = tipo_inscripcion
        if modalidad_pago:
            enrollment.modalidadPago = modalidad_pago
        if id_alumno:
            student = Alumno.objects.get(pk=id_alumno)
            enrollment.idAlumno = student
        if id_pago:
            payment = Pago.objects.get(pk=id_pago)
            enrollment.idPago = payment
        if id_usuario:
            user = get_user_model().objects.get(pk=id_usuario)
            enrollment.idUsuario = user

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
        id_alumno = graphene.Int()

    def mutate(self, info, carta_buena_conducta, certificado_primaria, curp_alumno, acta_nacimiento, observaciones, cda, autorizacion_irse_solo, autorizacion_publicitaria, atencion_psicologica, padecimiento, uso_aparato_auditivo, uso_de_lentes, lateralidad, id_alumno):
        student = Alumno.objects.get(pk=id_alumno)
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
