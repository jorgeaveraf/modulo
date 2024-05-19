import graphene
from graphene_django import DjangoObjectType
from .models import Inscripcion, Pago, Alumno, PadresTutores, AnexoAlumnos

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
    id_alumno = graphene.Field(StudentType)
    id_pago = graphene.Field(PaymentType)
    
class Mutation(graphene.ObjectType):
    create_student = CreateAlumno.Field()
    create_payment = CreatePago.Field()
    create_tutor = CreatePadresTutores.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)