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

'''class CreateAnexoAlumnos(graphene.Mutation):
fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('carta_buena_conducta', models.BooleanField(default=False)),
                ('certificado_primaria', models.BooleanField(default=False)),
                ('curp_alumno', models.BooleanField(default=False)),
                ('acta_nacimiento', models.BooleanField(default=False)),
                ('observaciones', models.TextField(blank=True)),
                ('cda', models.URLField(blank=True)),
                ('autorizacion_irse_solo', models.BooleanField(default=False)),
                ('autorizacion_publicitaria', models.BooleanField(default=False)),
                ('atencion_psicologica', models.BooleanField(default=False)),
                ('padecimiento', models.TextField(blank=True)),
                ('uso_aparato_auditivo', models.BooleanField(default=False)),
                ('uso_de_lentes', models.BooleanField(default=False)),
                ('lateralidad', models.CharField(max_length=1)),
                ('id_alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easyenroll.alumno')),
            ],
'''
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

class Mutation(graphene.ObjectType):
    create_student = CreateAlumno.Field()
    create_payment = CreatePago.Field()
    create_tutor = CreatePadresTutores.Field()
    create_enrollment = CreateInscripcion.Field()
    create_annex = createAnexoAlumnos.Field()
