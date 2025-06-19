import logging
import os
import uuid
from datetime import date, datetime
from django.utils import timezone 
import jwt
import requests
import time
import json

from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from bloodpoint_app.utils.export_helpers import generar_csv_resumen_campana
from bloodpoint_app.utils.excel_templates import generar_excel_campana
from bloodpoint_app.utils.exportar_top3_campanas_por_donaciones import exportar_top3_campanas_por_donaciones
from bloodpoint_app.utils.respuesta_donante import enviar_respuesta_a_donante
from bloodpoint_app.forms import AdminBPForm
from bloodpoint_app.forms import RepresentanteOrgForm
from django.views.generic import ListView

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    CustomUser,
    representante_org,
    donante,
    centro_donacion,
    donacion,
    solicitud_campana_repo,
    campana,
    adminbp,
    preguntas_usuario,
    respuestas_representante,
    AchievementDefinition,
    UserAchievement,
    UserStats
)

from .serializers import (
    CustomUserSerializer,
    RepresentanteOrgSerializer,
    DonantePerfilSerializer,
    DonacionSerializer,
    SolicitudCampanaSerializer,
    CentroDonacionSerializer,
    donanteSerializer,
    CampanaSerializer,
    AchievementDefinitionSerializer,
    UserAchievementSerializer,
    UserStatsSerializer
)

from bloodpoint_app.models import CustomUser as BP_CustomUser, donante as BP_donante
from bloodpoint_app import views
from .services import AchievementService
import logging


logger = logging.getLogger(__name__)


#def home_view(request):
#    return HttpResponse("Welcome to Bloodpoint API")

# NAVEGADOR 


@login_required
def listar_preguntas(request):
    representante = representante_org.objects.get(user=request.user)
    preguntas = preguntas_usuario.objects.filter(respondida=False)
    return render(request, 'representante/listar_preguntas.html', {'preguntas': preguntas})

@login_required
def responder_pregunta(request, pregunta_id):
    pregunta = get_object_or_404(preguntas_usuario, id=pregunta_id)
    representante = representante_org.objects.get(user=request.user)

    if request.method == 'POST':
        respuesta_texto = request.POST.get('respuesta')

        respuesta = respuestas_representante.objects.create(
            respuesta=respuesta_texto,
            fecha_respuesta=timezone.now(),
            id_pregunta=pregunta,
            id_representante=representante
        )

        pregunta.respondida = True
        pregunta.save()

        enviar_respuesta_a_donante(respuesta.id)
        return redirect('listar_preguntas')

    return render(request, 'representante/pregunta_chatbot.html', {'pregunta': pregunta})


##generador csv
def exportar_resumen_una_campana_csv(request, campana_id):
    csv_content = generar_csv_resumen_campana(campana_id)

    response = HttpResponse(
        csv_content,
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="campaña_{campana_id}.csv"'},
    )
    return response

def descargar_excel_campana(request, campana_id):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=resumen_campana_N°{campana_id}.xlsx'
    generar_excel_campana(campana_id, response)
    return response

def descargar_top3_campanas(request):
    excel_file = exportar_top3_campanas_por_donaciones()
    response = HttpResponse(
        excel_file,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"top3_campanas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response

def campanas(request):
    return render(request, 'campannas.html')

@login_required
def home(request):
    user = request.user
    print("USUARIO ACTUAL:", request.user, request.user.is_authenticated)
    return render(request, 'home.html')

def admin_home(request):
    user = request.user
    print("USUARIO ACTUAL:", request.user, request.user.is_authenticated)
    return render(request, 'admin_home.html')

def admin_index(request):
    admins = adminbp.objects.exclude(user_id=request.user.id)
    return render(request, 'administrador/index.html', {'admins': admins})

def detalles_admin(request, id):
    admin = get_object_or_404(adminbp, id_admin=id)
    admin_fields = vars(admin)  # Convert to a dictionary

    return render(request, 'administrador/detalles_admin.html', {'admin': admin, 'admin_fields': admin_fields})


# CREAR adminbp
def crear_admin(request):
    if request.method == 'POST':
        form = AdminBPForm(request.POST)
        if form.is_valid():
            # Extraer los datos del formulario
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            contrasena = form.cleaned_data['contrasena']

            # Crear el usuario base
            user = CustomUser.objects.create_user(
                email=email,
                password=contrasena,
                tipo_usuario='admin'
            )

            # Crear el perfil de adminbp vinculado
            adminbp.objects.create(
                user=user,
                nombre=nombre,
                email=email,
            )

            return redirect('admin_index')
    else:
        form = AdminBPForm()
        return render(request, 'administrador/crear_admin.html', {'form': form})

def editar_admin(request, id):
    admin = get_object_or_404(adminbp, id_admin=id)
    if request.method == 'POST':
        form = AdminBPForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('detalles_admin', id=id)
    else:
        form = AdminBPForm(instance=admin)
    return render(request, 'administrador/editar_admin.html', {'form': form, 'admin': admin})

def eliminar_admin(request, id):
    admin = get_object_or_404(adminbp, id_admin=id)
    admin.delete()
    return redirect('admin_index')

def configuracion_admin(request):
    admin = get_object_or_404(adminbp, user=request.user)
    return render(request, 'administrador/configuracion.html', {'admin': admin})

def editar_configuracion(request):
    admin = get_object_or_404(adminbp, user=request.user)
    if request.method == 'POST':
        form = AdminBPForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('configuracion_admin')
    else:
        form = AdminBPForm(instance=admin)
    return render(request, 'administrador/editar_configuracion.html', {'form': form, 'admin': admin})

def representante_index(request):
    representantes = representante_org.objects.filter(verificado=True)
    paginator = Paginator(representantes, 5) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'representante/index.html', {'page_obj': page_obj})

def detalles_representante(request, id):
    representante = get_object_or_404(representante_org, id_representante=id)
    representante_fields = vars(representante)  # Convert to a dictionary

    return render(request, 'representante/detalles_representante.html', {'representante': representante, 'representante_fields': representante_fields})

def verificar_representante(request, id):
    representante = get_object_or_404(representante_org, id_representante=id)
    representante.verificado = True
    representante.save()
    return redirect('lista_verificar')

def editar_representante(request, id):
    representante = get_object_or_404(representante_org, id_representante=id)
    if request.method == 'POST':
        form = RepresentanteOrgForm(request.POST, instance=representante)
        if form.is_valid():
            form.save()
            return redirect('detalles_representante', id=id)
    else:
        form = RepresentanteOrgForm(instance=representante)
    return render(request, 'representante/editar_representante.html', {'form': form, 'representante': representante})

def eliminar_representante(request, id):
    representante = get_object_or_404(representante_org, id_representante=id)
    representante.delete()
    return redirect('representante_index')

def configuracion_representante(request):
    representante = get_object_or_404(representante_org, user=request.user)
    return render(request, 'representante/configuracion.html', {'representante': representante})

def editar_configuracion_representante(request):
    representante = get_object_or_404(representante_org, user=request.user)
    
    if request.method == 'POST':
        form = RepresentanteOrgForm(request.POST, request.FILES, instance=representante)
        if form.is_valid():
            # Debug: Ver qué estamos recibiendo
            print("Archivos recibidos:", request.FILES)
            print("Datos del formulario:", request.POST)
            
            # Guardar instancia
            instance = form.save(commit=False)
            
            if 'credencial' in request.FILES:
                print("Nueva imagen recibida:", request.FILES['credencial'])
                # Forzar la actualización del campo
                instance.credencial = request.FILES['credencial']
            
            instance.save()
            print("Imagen guardada. URL:", instance.credencial.url if instance.credencial else "No hay imagen")
            
            return redirect('configuracion_representante')
        else:
            print("Errores en el formulario:", form.errors)
    else:
        form = RepresentanteOrgForm(instance=representante)
    
    return render(request, 'administrador/editar_configuracion.html', {
        'form': form,
        'representante': representante
    })

def lista_verificar(request):
    representantes = representante_org.objects.filter(verificado=False)
    paginator = Paginator(representantes, 5) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'representante/lista_verificar.html', {'page_obj': page_obj})

def detalles_verificar(request, id):
    representante = get_object_or_404(representante_org, id_representante=id)

    return render(request, 'representante/detalles_verificar.html', {'representante': representante})

def campana_index(request):
    
    representante = representante_org.objects.get(user=request.user)
    campanas = campana.objects.filter(id_representante=representante.id_representante)
    paginator = Paginator(campanas, 5) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'campanas/index.html', {'page_obj': page_obj})

def detalles_campana(request, id):
    campana_ojb = get_object_or_404(campana, id_campana=id)
    return render(request, 'campanas/detalles_campana.html', {'campana_ojb': campana_ojb})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()  # Campo obligatorio
        password = request.POST.get('password')
        
        # Autentica SOLO si es representante o admin (usa EmailAuthBackend o ModelBackend)
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # Verifica que no sea un donante
            if user.tipo_usuario in ['representante', 'admin']:
                login(request, user)
                if user.tipo_usuario == 'admin':
                    return redirect('admin_home')  # redirige al home de admin
                else:
                    return redirect('home')  # home normal para representante u otro
            else:
                messages.error(request, 'Solo representantes/admins pueden acceder por aquí.')
        else:
            messages.error(request, 'Email o contraseña incorrectos.')
    
    return render(request, 'login.html')  # Template genérico (ajusta el nombre si es necesario)



def signup_representante(request):
    if request.method == 'POST':
        # Extraer datos del formulario
        rut = request.POST.get('rut_representante', '').strip()
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        rol = request.POST.get('rol', '').strip()
        credencial = request.FILES.get('credencial')
        
        # Validaciones básicas
        if not rut:
            return render(request, 'signup.html', {'error': 'El RUT es obligatorio'})
        
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Este correo ya está registrado'})
    
        if not nombre:
            return render(request, 'signup.html', {'error': 'El nombre es obligatorio'})
            
        if not apellido:
            return render(request, 'signup.html', {'error': 'El apellido es obligatorio'})
        if not email:
            return render(request, 'signup.html', {'error': 'El correo electrónico es obligatorio'})
            
        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Las contraseñas no coinciden'})
        
        if len(password1) < 8:
            return render(request, 'signup.html', {'error': 'La contraseña debe tener al menos 8 caracteres'})
            
        # Limpiar formato del RUT 
        rut = rut.replace('.', '').replace(' ', '')

        # Verificar si el usuario ya existe
        if CustomUser.objects.filter(rut=rut).exists() or CustomUser.objects.filter(email=email).exists(): 
            return render(request, 'signup.html', {'error': 'Este email ya está registrado'})
        
        try:
            # Usamos transaction.atomic para asegurarnos de que ambas operaciones se ejecuten o fallen juntas
            with transaction.atomic():
                # Crear el usuario primero
                user = CustomUser.objects.create_user(
                    rut=None,
                    email=email,
                    password=password1,
                    tipo_usuario='representante'
                )
                user.save()
                
                # Luego crear el representante vinculado al usuario
                representante = representante_org(
                    user=user,
                    rut_representante=rut,
                    rol=rol,
                    nombre=nombre,
                    apellido=apellido
                )
                
                if credencial:
                    representante.credencial = credencial
                    
                representante.save()
                
                # Redirigir al login
                return redirect('login')
                
        except IntegrityError as e:
            # Para debugging, puedes imprimir el error
            print(f"Error de integridad: {e}")
            return render(request, 'signup.html', {'error': 'Error al registrar: ya existe un usuario con este RUT o correo'})
        except Exception as e:
            # Captura cualquier otro tipo de error
            print(f"Error inesperado: {e}")
            return render(request, 'signup.html', {'error': f'Error inesperado: {str(e)}'})
    
    # Si es GET, mostrar el formulario vacío
    return render(request, 'signup.html')


def logout_view(request):
    logout(request)
    return redirect('login')

#APP MOVIL
@api_view(['GET', 'POST'])
def centros_listado(request):
    if request.method == 'GET':
        # Verificar si se solicitan solo los centros del representante
        representante_filter = request.query_params.get('representante', 'false').lower() == 'true'
        
        if representante_filter:
            # Verificar si el usuario está autenticado y es un representante
            if not request.user.is_authenticated:
                return Response({
                    "status": "error",
                    "message": "Usuario no autenticado."
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                representante = representante_org.objects.get(user=request.user)
                centros = centro_donacion.objects.filter(id_representante=representante)
            except representante_org.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "El usuario no es un representante."
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            # Si no se especifica el filtro, mostrar todos los centros
            centros = centro_donacion.objects.all()
            
        
        withcampanas = request.query_params.get('campanas', 'false').lower() == 'true'
        resultado = []
        if withcampanas:
            for centro in centros:
                campanas = campana.objects.filter(id_centro=centro)
                campanas_serializer = CampanaSerializer(campanas, many=True)
            centro_data = {
                "id_centro": centro.id_centro,
                "nombre_centro": centro.nombre_centro,
                "direccion_centro": centro.direccion_centro,
                "comuna": centro.comuna,
                "telefono": centro.telefono,
                "horario_apertura": centro.horario_apertura,
                "horario_cierre": centro.horario_cierre,
                "campanas": campanas_serializer.data
            }
            resultado.append(centro_data)
        else:
            serializer = CentroDonacionSerializer(centros, many=True)
            resultado = serializer.data
        return Response({
            "status": "success",
            "count": centros.count(),
            "data": resultado
        })

    elif request.method == 'POST':
        serializer = CentroDonacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def centro_detail(request, id):
    try:
        centro = centro_donacion.objects.get(id_centro=id)
    except centro_donacion.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Centro no encontrado."
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CentroDonacionSerializer(centro)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CentroDonacionSerializer(centro, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        centro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def list_representantes(request):
    representantes = representante_org.objects.all()
    serializer = RepresentanteOrgSerializer(representantes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def register_representante(request):
    email = request.data.get("email")
    password = request.data.get("contrasena")

    if not email or email.strip() == '':
        return Response({
            "status": "error",
            "message": "El campo email no puede estar vacío."
        }, status=400)

    if CustomUser.objects.filter(email=email).exists():
        return Response({
            "status": "error",
            "message": "El email ya está registrado."
        }, status=400)

    # Generar un rut tipo REP-<uuid>
    rut_generado = f"REP-{uuid.uuid4().hex[:10]}"

    user = CustomUser.objects.create_user(
        rut=rut_generado,
        email=email,
        password=password,
        tipo_usuario='representante'
    )

    # Crear representante ligado al usuario
    representante = representante_org.objects.create(
        user=user,
        rol=request.data.get("rol"),
        nombre=request.data.get("nombre"),
    )

    return Response({
        "status": "created",
        "user_id": user.id,
        "representante_id": representante.id_representante,
    }, status=201)

@api_view(['GET'])
def representante_detail(request, id):
    try:
        representante = representante_org.objects.get(user__id=id)
        return Response({
            "id_representante": representante.id_representante,
            "nombre": representante.nombre,
            "rol": representante.rol,
            "user_id": representante.user.id,
            "is_representante": True
        })
    except representante_org.DoesNotExist:
        return Response({"is_representante": False}, status=200)

@api_view(['POST'])
def ingresar(request):
    rut = request.data.get('rut')
    email = request.data.get('email')
    password = request.data.get('password')

    user = None

    if rut:
        # Login para donantes
        user = authenticate(request, rut=rut, password=password)
        print(user, request, password)
    elif email:
        # Login para representantes
        try:
            user = CustomUser.objects.get(email=email, tipo_usuario='representante')
            if not user.check_password(password):
                user = None
        except CustomUser.DoesNotExist:
            user = None

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'status': 'success',
            'token': token.key,
            'user_id': user.id,
            'tipo_usuario': user.tipo_usuario,
        })
    else:
        return Response({
            'status': 'error',
            'message': 'Credenciales incorrectas.'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def register(request):
    # Obtener datos enviados por el usuario
    rut = request.data.get("rut")
    email = request.data.get("email")
    password = request.data.get("contrasena")

    # Validar si el rut está vacío
    if not rut or rut.strip() == '':
        return Response({
            "status": "error",
            "message": "El campo rut no puede estar vacío."
        }, status=400)

    # Validar si el rut ya existe
    if CustomUser.objects.filter(rut=rut).exists():
        return Response({
            "status": "error",
            "message": "El rut ya está registrado."
        }, status=400)

    # Crear usuario en CustomUser con tipo_usuario = "donante"
    user = CustomUser.objects.create_user(
        rut=rut,
        email=email,
        password=password,
        tipo_usuario='donante'
    )

    # Resto de los datos para crear el objeto donante
    donante_data = {
        "rut": rut,
        "nombre_completo": request.data.get("nombre_completo"),
        "ocupacion": request.data.get("ocupacion"),
        "direccion": request.data.get("direccion"),
        "comuna": request.data.get("comuna"),
        "fono": request.data.get("fono"),
        "sexo": request.data.get("sexo"),
        "fecha_nacimiento": request.data.get("fecha_nacimiento"),
        "nacionalidad": request.data.get("nacionalidad"),
        "tipo_sangre": request.data.get("tipo_sangre"),
        "dispo_dia_donacion": request.data.get("dispo_dia_donacion"),
        "nuevo_donante": request.data.get("nuevo_donante"),
        "noti_emergencia": request.data.get("noti_emergencia"),
        "user": user  # Vincula el usuario creado
    }

    donante_obj = donante.objects.create(**donante_data)

    # Check for achievements after user registration
    try:
        new_achievements = AchievementService.check_and_award_achievements(donante_obj)
        if new_achievements:
            achievement_serializer = AchievementDefinitionSerializer(new_achievements, many=True)
            return Response({
                "status": "created",
                "user_id": user.id,
                "donante_id": donante_obj.id_donante,
                "new_achievements": achievement_serializer.data
            }, status=201)
    except Exception as e:
        logger.warning(f"Achievement check failed for new user {donante_obj.id_donante}: {e}")

    return Response({
        "status": "created",
        "user_id": user.id,
        "donante_id": donante_obj.id_donante,
    }, status=201)



@api_view(['GET', 'PUT'])
def profile(request):
    if not request.user.is_authenticated:
        return Response({
            "status": "error",
            "message": "Usuario no autenticado."
        }, status=403)

    # obtenemos el objeto donante relacionado con el usuario
    try:
        donante_obj = donante.objects.get(user=request.user)
    except donante.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Perfil de donante no encontrado."
        }, status=404)

    if request.method == 'GET':
        # Usamos el nuevo serializer combinado
        serializer = DonantePerfilSerializer(donante_obj)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=200)

    elif request.method == 'PUT':
        serializer = DonantePerfilSerializer(donante_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Perfil actualizado exitosamente.",
                "data": serializer.data
            }, status=200)
        else:
            return Response({
                "status": "error",
                "errors": serializer.errors
            }, status=400)


@api_view(['GET', 'POST'])
def donantes_listado(request):

    if request.method == 'GET':
        
        donantes = donante.objects.all()
        
        serializer = donanteSerializer(donantes, many=True)
        
        return Response({
            "status": "success",
            "count": donantes.count(),
            "data": serializer.data
        })
    elif request.method == 'POST':
        serializer = donanteSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        # Explicit return for invalid data
        return Response(
            {
                "status": "error",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'PUT', 'DELETE'])
def donante_detail(request, id):

    try:
        donante_obj = donante.objects.get(id_donante=id)
    except donante.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = donanteSerializer(donante_obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = donanteSerializer(donante_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        donante_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def registrar_donacion(request):
    if not request.user.is_authenticated:
        return Response({
            "status": "error",
            "message": "Usuario no autenticado."
        }, status=403)

    try:
        donante_obj = donante.objects.get(user=request.user)
    except donante.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Donante no encontrado."
        }, status=404)

    centro_id = request.data.get("centro_id")
    fecha_str = request.data.get("fecha_donacion")

    if not centro_id or not fecha_str:
        return Response({
            "status": "error",
            "message": "Los campos 'centro_id' y 'fecha_donacion' son obligatorios."
        }, status=400)

    try:
        centro = centro_donacion.objects.get(id_centro=centro_id)
    except centro_donacion.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Centro de donación no encontrado."
        }, status=404)

    try:
        fecha_donacion = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({
            "status": "error",
            "message": "Formato de fecha inválido. Use 'YYYY-MM-DD'."
        }, status=400)

    if fecha_donacion < date.today():
        return Response({
            "status": "error",
            "message": "La fecha de donación no puede ser anterior a hoy."
        }, status=400)
        
    campana_id = request.data.get("campana_id")
    solicitud_id = request.data.get("solicitud_id")

    if campana_id and solicitud_id:
        return Response({
            "status": "error",
            "message": "Una donación no puede estar asociada a campaña y solicitud al mismo tiempo."
        }, status=400)
    
    tipo_donacion = 'punto'
    if campana_id:
        tipo_donacion = 'campana'
    elif solicitud_id:
        tipo_donacion = 'solicitud'

    nueva_donacion = donacion.objects.create(
        id_donante=donante_obj,
        centro_id=centro,
        fecha_donacion=fecha_donacion,
        cantidad_donacion=1,
        campana_relacionada=campana.objects.get(id_campana=campana_id) if campana_id else None,
        solicitud_relacionada=solicitud_campana_repo.objects.get(id_solicitud=solicitud_id) if solicitud_id else None,
        tipo_donacion=tipo_donacion
)


    # Check for achievements after donation registration
    response_data = {
        "status": "success",
        "message": "Donación registrada exitosamente.",
        "donacion_id": nueva_donacion.id_donacion,
        "fecha_donacion": nueva_donacion.fecha_donacion.isoformat(),
        "centro": centro.nombre_centro
    }
    
    try:
        new_achievements = AchievementService.check_and_award_achievements(donante_obj)
        if new_achievements:
            achievement_serializer = AchievementDefinitionSerializer(new_achievements, many=True)
            response_data["new_achievements"] = achievement_serializer.data
    except Exception as e:
        logger.warning(f"Achievement check failed for donation {nueva_donacion.id_donacion}: {e}")

    return Response(response_data, status=201)

@api_view(['GET'])
def historial_donaciones(request):
    if not request.user.is_authenticated:
        return Response({
            "status": "error",
            "message": "Usuario no autenticado."
        }, status=status.HTTP_403_FORBIDDEN)

    try:
        donante_obj = donante.objects.get(user=request.user)
    except donante.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Donante no encontrado."
        }, status=status.HTTP_404_NOT_FOUND)

    donaciones = donacion.objects.filter(id_donante=donante_obj).order_by('-fecha_donacion')

    # Record history view for achievements (do this in a try-catch to not break the main flow)
    try:
        AchievementService.record_history_view(donante_obj)
    except Exception as e:
        logger.warning(f"Failed to record history view for donante {donante_obj.id_donante}: {e}")

    serializer = DonacionSerializer(donaciones, many=True)
    return Response({
        "status": "success",
        "donaciones": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def crear_solicitud_campana(request):
    if not request.user.is_authenticated:
        return Response({"status": "error", "message": "No autenticado"}, status=403)

    try:
        donante_obj = donante.objects.get(user=request.user)
    except donante.DoesNotExist:
        return Response({"status": "error", "message": "Donante no encontrado"}, status=404)

    data = request.data.copy()
    data['id_donante'] = donante_obj.id_donante

    serializer = SolicitudCampanaSerializer(data=data)
    if serializer.is_valid():
        solicitud = serializer.save()

        # Crear campaña directamente al crear la solicitud
        nueva_campana = campana.objects.create(
            nombre_campana=solicitud.nombre_campana,
            fecha_campana=solicitud.fecha_solicitud,
            fecha_termino=solicitud.fecha_termino,
            id_centro=solicitud.centro_donacion,
            apertura=request.data.get("apertura"),
            cierre=request.data.get("cierre"),
            meta=str(solicitud.cantidad_personas),
            latitud=request.data.get("latitud", ""),
            longitud=request.data.get("longitud", ""),
            id_solicitud=solicitud,
            validada=True  # o False si quieres que los reps validen después
        )

        solicitud.estado = 'aprobado'  # O mantener en 'pendiente'
        solicitud.campana_asociada = nueva_campana
        solicitud.save()

        return Response({
            "status": "success",
            "data": serializer.data,
            "campana_creada": nueva_campana.id_campana
        }, status=201)

    return Response({"status": "error", "errors": serializer.errors}, status=400)

@api_view(['POST'])
def crear_campana(request):
    if not request.user.is_authenticated:
        return Response({"status": "error", "message": "No autenticado"}, status=403)

    try:
        representante = representante_org.objects.get(user=request.user)
    except representante_org.DoesNotExist:
        return Response({"status": "error", "message": "Solo representantes pueden crear campañas"}, status=403)

    data = request.data.copy()

    # Validación básica
    required_fields = ['fecha_campana', 'fecha_termino', 'id_centro', 'apertura', 'cierre', 'meta']
    for field in required_fields:
        if field not in data:
            return Response({"status": "error", "message": f"Campo requerido: {field}"}, status=400)

    try:
        centro = centro_donacion.objects.get(id_centro=data['id_centro'])
    except centro_donacion.DoesNotExist:
        return Response({"status": "error", "message": "Centro no encontrado"}, status=404)

    camp = campana.objects.create(
        nombre_campana=data['nombre_campana'],
        fecha_campana=data['fecha_campana'],
        fecha_termino=data['fecha_termino'],
        id_centro=centro,
        apertura=data['apertura'],
        cierre=data['cierre'],
        meta=data['meta'],
        latitud=data.get('latitud', ''),
        longitud=data.get('longitud', ''),
        id_representante=representante,
        validada=True
    )

    return Response({
        "status": "success",
        "message": "Campaña creada exitosamente.",
        "id_campana": camp.id_campana
    }, status=201)

@api_view(['PUT'])
def validar_campana(request, campana_id):
    if not request.user.is_authenticated:
        return Response({"status": "error", "message": "No autenticado"}, status=403)

    try:
        representante = representante_org.objects.get(user=request.user)
    except representante_org.DoesNotExist:
        return Response({"status": "error", "message": "Solo representantes pueden validar campañas"}, status=403)

    try:
        camp = campana.objects.get(id_campana=campana_id)
    except campana.DoesNotExist:
        return Response({"status": "error", "message": "Campaña no encontrada"}, status=404)

    camp.validada = True
    camp.id_representante = representante  # También puedes dejar constancia del representante que la validó
    camp.save()

    return Response({"status": "success", "message": "Campaña validada"}, status=200)

@api_view(['GET'])
def listar_solicitudes_campana(request):
    if not request.user.is_authenticated:
        return Response({"status": "error", "message": "No autenticado"}, status=403)

    try:
        representante_org.objects.get(user=request.user)
    except representante_org.DoesNotExist:
        return Response({"status": "error", "message": "Solo los representantes pueden ver las solicitudes"}, status=403)

    solicitudes = solicitud_campana_repo.objects.all().order_by('-created_at')
    serializer = SolicitudCampanaSerializer(solicitudes, many=True)

    return Response({"status": "success", "data": serializer.data}, status=200)

@api_view(['GET'])
def progreso_campana(request, campana_id):
    try:
        camp = campana.objects.get(id_campana=campana_id)
    except campana.DoesNotExist:
        return Response({"status": "error", "message": "Campaña no encontrada"}, status=404)

    total = donacion.objects.filter(solicitud_relacionada=camp.id_solicitud).count()

    return Response({
        "status": "success",
        "meta": camp.meta,
        "donaciones_actuales": total
    })
    
@api_view(['PUT'])
def validar_donacion(request, donacion_id):
    try:
        representante = representante_org.objects.get(user=request.user)
    except representante_org.DoesNotExist:
        return Response({"status": "error", "message": "Solo representantes pueden validar donaciones"}, status=403)

    try:
        don = donacion.objects.get(id_donacion=donacion_id)
    except donacion.DoesNotExist:
        return Response({"status": "error", "message": "Donación no encontrada"}, status=404)

    if don.validada:
        return Response({"status": "warning", "message": "La donación ya está validada"}, status=200)

    don.validada = True
    don.save()

    return Response({"status": "success", "message": "Donación validada"}, status=200)

@api_view(['GET'])
def donaciones_pendientes(request, rut):
    try:
        donante_obj = donante.objects.get(rut=rut)
    except donante.DoesNotExist:
        return Response({"status": "error", "message": "Donante no encontrado"}, status=404)

    donaciones = donacion.objects.filter(id_donante=donante_obj, validada=False).order_by('-fecha_donacion')

    serializer = DonacionSerializer(donaciones, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(['POST'])
def registrar_intencion_donacion(request):
    if not request.user.is_authenticated:
        return Response({"status": "error", "message": "No autenticado"}, status=403)

    try:
        donante_obj = donante.objects.get(user=request.user)
    except donante.DoesNotExist:
        return Response({"status": "error", "message": "Donante no encontrado"}, status=404)

    campana_id = request.data.get("campana_id")

    if not campana_id:
        return Response({"status": "error", "message": "campana_id es requerido"}, status=400)

    try:
        campana_obj = campana.objects.get(id_campana=campana_id)
    except campana.DoesNotExist:
        return Response({"status": "error", "message": "Campaña no encontrada"}, status=404)

    # Registrar intención
    donacion.objects.create(
        id_donante=donante_obj,
        centro_id=campana_obj.id_centro,
        fecha_donacion=campana_obj.fecha_campana,
        cantidad_donacion=1,
        tipo_donacion='campana',
        campana_relacionada=campana_obj,
        es_intencion=True
    )

    # Check for achievements after intention registration
    response_data = {"status": "success", "message": "Intención registrada"}
    
    try:
        new_achievements = AchievementService.check_and_award_achievements(donante_obj)
        if new_achievements:
            achievement_serializer = AchievementDefinitionSerializer(new_achievements, many=True)
            response_data["new_achievements"] = achievement_serializer.data
    except Exception as e:
        logger.warning(f"Achievement check failed for intention by donante {donante_obj.id_donante}: {e}")

    return Response(response_data, status=201)

@api_view(['GET'])
def estado_donaciones_campana(request, campana_id):
    try:
        camp = campana.objects.get(id_campana=campana_id)
    except campana.DoesNotExist:
        return Response({"status": "error", "message": "Campaña no encontrada"}, status=404)

    donaciones = donacion.objects.filter(campana_relacionada=camp)

    completadas = donaciones.filter(validada=True).count()
    no_completadas = donaciones.filter(validada=False).count()

    return Response({
        "status": "success",
        "meta": camp.meta,
        "completadas": completadas,
        "no_completadas": no_completadas,
    })

@api_view(['POST'])
def escanear_qr_donacion(request):
    rut = request.data.get("rut")
    centro_id = request.data.get("centro_id")
    tipo_donacion = request.data.get("tipo_donacion")  # punto | campana | solicitud
    campana_id = request.data.get("campana_id")
    solicitud_id = request.data.get("solicitud_id")

    if not request.user.is_authenticated:
        return Response({"status": "error", "message": "No autenticado"}, status=403)

    if not rut or not centro_id or not tipo_donacion:
        return Response({"status": "error", "message": "Campos obligatorios: rut, centro_id, tipo_donacion"}, status=400)

    try:
        representante = representante_org.objects.get(user=request.user)
    except representante_org.DoesNotExist:
        return Response({"status": "error", "message": "Solo representantes pueden registrar donaciones"}, status=403)

    try:
        donante_obj = donante.objects.get(rut=rut)
    except donante.DoesNotExist:
        return Response({"status": "error", "message": "Donante no encontrado"}, status=404)

    try:
        centro = centro_donacion.objects.get(id_centro=centro_id)
    except centro_donacion.DoesNotExist:
        return Response({"status": "error", "message": "Centro no encontrado"}, status=404)

    campana_obj = None
    solicitud_obj = None

    if tipo_donacion == 'campana':
        if not campana_id:
            return Response({"status": "error", "message": "campana_id es requerido para tipo campana"}, status=400)
        try:
            campana_obj = campana.objects.get(id_campana=campana_id)
        except campana.DoesNotExist:
            return Response({"status": "error", "message": "Campaña no encontrada"}, status=404)
    elif tipo_donacion == 'solicitud':
        if not solicitud_id:
            return Response({"status": "error", "message": "solicitud_id es requerido para tipo solicitud"}, status=400)
        try:
            solicitud_obj = solicitud_campana_repo.objects.get(id_solicitud=solicitud_id)
        except solicitud_campana_repo.DoesNotExist:
            return Response({"status": "error", "message": "Solicitud no encontrada"}, status=404)

    # Crear la donación
    nueva = donacion.objects.create(
        id_donante=donante_obj,
        centro_id=centro,
        fecha_donacion=date.today(),
        cantidad_donacion=1,
        tipo_donacion=tipo_donacion,
        campana_relacionada=campana_obj,
        solicitud_relacionada=solicitud_obj,
        validada=True
    )

    return Response({
        "status": "success",
        "message": "Donación registrada y validada por QR",
        "donacion_id": nueva.id_donacion,
        "fecha": nueva.fecha_donacion.isoformat(),
        "tipo": tipo_donacion
    }, status=201)
    
@api_view(['GET'])
def campanas_activas(request):
    hoy = date.today()
    campanas = campana.objects.filter(validada=True, fecha_campana__lte=hoy, fecha_termino__gte=hoy)
    serializer = CampanaSerializer(campanas, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=200)

@api_view(['POST'])
def ask_bot(request):
    try:
        # Get question from either GET parameters or POST body
        if request.method == "GET":
            question = request.GET.get("prompt")
        elif request.method == "POST":
            try:
                data = json.loads(request.body)
                question = data.get("prompt")
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON in request body"}, status=400)
        else:
            return Response({"error": "Método no permitido"}, status=405)

        if not question:
            return Response({"error": "Falta el parámetro 'prompt'"}, status=400)

        # Validación con modelo
        resultado_validacion = validar_con_modelo(question)

        if resultado_validacion == "no":
            return Response({
                "validacion": "no",
                "response": "Por favor, realiza una pregunta relacionada con la donación de sangre."
            })

        elif resultado_validacion == "idk":
            return Response({
                "validacion": "idk",
                "response": "No estoy seguro si tu pregunta está relacionada. ¿Podrías reformularla?"
            })

        # Si pasó la validación
        headers = {
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
            "X-Title": "Chatbot Donación de Sangre",
            "OpenAI-Organization": "org-123456789"  # Adding organization header
        }

        # Obtener el archivo BPCB.json
        with open('bloodpoint_app/BPCB.json', 'r') as file:
            bpcb_data = json.load(file)

        # Crear el prompt completo
        full_question = create_full_question(question, bpcb_data)

        body = {
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [
                {"role": "system", "content": "Eres un asistente especializado en donación de sangre."},
                {"role": "user", "content": full_question["prompt"]}
            ]
        }

        print("Sending request to OpenRouter with headers:", headers)  # Debug print
        openrouter_response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=body
        )

        result = openrouter_response.json()
        print("OpenRouter Response:", result)  # Debug print

        # Extraer el texto limpio de la respuesta del modelo
        answer = result.get("choices", [{}])[0].get("message", {}).get("content", "Sin respuesta generada.").strip()

        # Devolver respuesta con formato estructurado
        return Response({
            "validacion": resultado_validacion,
            "response": answer,
        })

    except Exception as e:
        print("Error in ask_bot:", str(e))  # Debug print
        return Response({"error": str(e)}, status=500)
    
def validar_con_modelo(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
        "X-Title": "Chatbot Donación de Sangre",
        "OpenAI-Organization": "org-123456789"  # Adding organization header
    }

    body = {
        "model": "deepseek/deepseek-chat-v3-0324:free",  # o cualquier otro modelo gratuito
        "messages": [
            {"role": "system", "content": "Responde únicamente con una de estas opciones: 'yes', 'no' o 'idk'. ¿La siguiente pregunta está relacionada con la donación de sangre?"},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        print("Validator sending request with headers:", headers)  # Debug print
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        result = response.json()
        print("Validator Response:", result)  # Debug print
        message = result.get("choices", [{}])[0].get("message", {}).get("content", "").lower().strip()

        if "yes" in message:
            return "yes"
        elif "idk" in message:
            return "idk"
        elif "no" in message:
            return "no"
        else:
            return prompt

    except Exception as e:
        print("Error en validador:", e)
        return "idk"

def create_full_question(question, bpcb_data):
    """
    Creates a full question prompt using the BPCB.json data
    """
    # Get the first document's data
    doc_data = bpcb_data[0]
    
    # Create the base prompt
    prompt = f"""Eres un asistente especializado en como .

Contexto: {doc_data['descripcion']}

Base de conocimiento sobre donación de sangre:
"""
    
    # Add all FAQ entries as context
    for faq in doc_data['faq']:
        prompt += f"\nPregunta: {faq['pregunta']}\nRespuesta: {faq['respuesta']}\n"
    
    # Add the current question
    prompt += f"\nPregunta actual: {question}\n"
    
    # Add instructions
    prompt += """
Por favor, responde la pregunta actual basándote en la información proporcionada.
Si la pregunta no está directamente relacionada con el contexto de donación de sangre,
indica que tu conocimiento está limitado a este tema específico.

ex: pregunta : ¿Qué regula la Norma 0146?
    respuesta: Regula el procedimiento de atención a donantes de sangre en lugares fijos (centros de sangre) o móviles (colectas móviles).
"""
    
    return {
        "question": question,
        "prompt": prompt
    }


#=========================================================== APACHE SUPERSET ==============================================================
from django.http import JsonResponse
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET

@require_GET
def generate_guest_token(request, chart_id):
    """
    Generates a JWT token for Superset embedded charts.
    Args:
        chart_id: ID of the Superset chart/dashboard to embed
    Returns:
        JsonResponse: { "token": "jwt.token.here", "exp": "iso-timestamp" }
        or error if validation fails.
    """
    try:
        # Validate chart_id exists (adjust based on your Superset API)
        if not chart_id:
            return HttpResponseBadRequest("Chart ID is required")

        # Prepare payload
        payload = {
            "user": {
                "username": "guest_embed",
                "first_name": "Guest",
                "last_name": "User",
                "roles": ["Gamma"]  # Required by Superset
            },
            "resources": [{
                "type": "explore",  # Use "dashboard" for dashboards
                "id": str(chart_id)  # Ensure string format
            }],
            "rls": [],  # Row Level Security rules (empty for full access)
            "aud": settings.SUPERSET_JWT_AUDIENCE,  # Must match Superset's config
            "iss": settings.SUPERSET_JWT_ISSUER,    # Your Heroku app identifier
            "exp": datetime.utcnow() + timedelta(seconds=settings.SUPERSET_JWT_EXP_SECONDS)
        }

        # Generate token
        token = jwt.encode(
            payload,
            settings.SUPERSET_JWT_SECRET,
            algorithm=settings.SUPERSET_JWT_ALGO
        )

        return JsonResponse({
            "token": token,
            "exp": payload["exp"].isoformat()
        })

    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "details": "Token generation failed"
        }, status=500)

# ACHIEVEMENT ENDPOINTS

@api_view(['GET'])
def user_achievements(request):
    """Return all achievement definitions with user completion status."""
    if not hasattr(request.user, 'donante'):
        return Response({'error': 'Only donors can have achievements'}, status=400)
    try:
        donante_obj = request.user.donante

        # Fetch user achievements via service
        user_achievements = AchievementService.get_user_achievements(donante_obj)
        completed_keys = {ua.achievement.key for ua in user_achievements}

        # Fetch all definitions
        all_defs = AchievementDefinition.objects.all()

        # Build response
        result = []
        for definition in all_defs:
            result.append({
                'name': definition.name,
                'key': definition.key,
                'symbol': definition.symbol,
                'description': definition.description,
                'category': definition.category,
                'user_completed': definition.key in completed_keys
            })

        return Response(result)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def user_stats(request):
    """Get user statistics"""
    if not hasattr(request.user, 'donante'):
        return Response({'error': 'Only donors have stats'}, status=400)
    
    try:
        donante_obj = request.user.donante
        stats = AchievementService.get_or_create_user_stats(donante_obj)
        AchievementService.update_user_stats(donante_obj)
        stats.refresh_from_db()
        serializer = UserStatsSerializer(stats)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def record_app_share(request):
    """Record that the user shared the app"""
    if not hasattr(request.user, 'donante'):
        return Response({'error': 'Only donors can share the app'}, status=400)
    
    try:
        donante_obj = request.user.donante
        new_achievements = AchievementService.record_app_share(donante_obj)
        
        if new_achievements:
            achievement_serializer = AchievementDefinitionSerializer(new_achievements, many=True)
            return Response({
                'message': 'App share recorded',
                'new_achievements': achievement_serializer.data
            })
        else:
            return Response({'message': 'App share recorded'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])  
def record_history_view(request):
    """Record that the user viewed their donation history"""
    if not hasattr(request.user, 'donante'):
        return Response({'error': 'Only donors can view history'}, status=400)
    
    try:
        donante_obj = request.user.donante
        new_achievements = AchievementService.record_history_view(donante_obj)
        
        if new_achievements:
            achievement_serializer = AchievementDefinitionSerializer(new_achievements, many=True)
            return Response({
                'message': 'History view recorded',
                'new_achievements': achievement_serializer.data
            })
        else:
            return Response({'message': 'History view recorded'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def unnotified_achievements(request):
    """Get achievements that haven't been notified yet"""
    if not hasattr(request.user, 'donante'):
        return Response({'error': 'Only donors can have achievements'}, status=400)
    
    try:
        donante_obj = request.user.donante
        achievements = AchievementService.get_unnotified_achievements(donante_obj)
        serializer = UserAchievementSerializer(achievements, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def mark_achievements_notified(request):
    """Mark achievements as notified"""
    if not hasattr(request.user, 'donante'):
        return Response({'error': 'Only donors can have achievements'}, status=400)
    
    try:
        achievement_ids = request.data.get('achievement_ids', [])
        if not achievement_ids:
            return Response({'error': 'achievement_ids required'}, status=400)
        
        AchievementService.mark_achievements_as_notified(achievement_ids)
        return Response({'message': 'Achievements marked as notified'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
