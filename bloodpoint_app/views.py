import logging
import uuid
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import donanteSerializer, CentroDonacionSerializer
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from bloodpoint_app.models import CustomUser, donante
from .models import CustomUser, representante_org, donante, centro_donacion, donacion, solicitud_campana_repo, campana
from .serializers import CustomUserSerializer, RepresentanteOrgSerializer, DonantePerfilSerializer, DonacionSerializer, SolicitudCampanaSerializer
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import uuid
from bloodpoint_app import views
from django.db import IntegrityError, transaction
from django.contrib import messages

from .models import centro_donacion, CustomUser, donacion, donante, representante_org, adminbp
from .serializers import (CentroDonacionSerializer,CustomUserSerializer,DonacionSerializer,DonantePerfilSerializer,RepresentanteOrgSerializer,donanteSerializer)

from bloodpoint_app import views

logger = logging.getLogger(__name__)

#def home_view(request):
#    return HttpResponse("Welcome to Bloodpoint API")

# NAVEGADOR 

def campanas(request):
    return render(request, 'campannas.html')

def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            tipo = user.tipo_usuario

            if tipo == 'representante':
                try:
                    representante = representante_org.objects.get(user=user)
                except representante_org.DoesNotExist:
                    messages.error(request, 'No se encontró el perfil del representante.')
                    return render(request, 'login.html')
                login(request, user)
                return redirect('home') 

            elif tipo == 'admin':
                try:
                    admin = adminbp.objects.get(email=user.email)
                except adminbp.DoesNotExist:
                    messages.error(request, 'No se encontró el perfil del administrador.')
                    return render(request, 'login.html')
                login(request, user)
                return redirect('home')  

            else:
                messages.error(request, 'Tipo de usuario no autorizado.')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'login.html')


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

@login_required
def listar_representantes(request):
    representantes = representante_org.objects.all()
    return render(request, 'representantes/listar.html', {'representantes': representantes})

@login_required
def editar_representante(request, id):
    representante = get_object_or_404(representante_org, id_representante=id)

    if request.method == 'POST':
        representante.nombre = request.POST.get('nombre')
        representante.apellido = request.POST.get('apellido')
        representante.rol = request.POST.get('rol')

        credencial = request.FILES.get('credencial')
        if credencial:
            representante.credencial = credencial

        representante.save()
        return redirect('listar_representantes')  # O donde quieras redirigir

    return render(request, 'representantes/editar.html', {'representante': representante})

@login_required
def eliminar_representante(request, id):
    representante = get_object_or_404(representante_org, id_representante=id)

    if request.method == 'POST':
        representante.delete()
        return redirect('listar_representantes')

    return render(request, 'representantes/eliminar_confirmacion.html', {'representante': representante})


# CREAR adminbp
def crear_admin(request):
    if request.method == 'POST':
        form = AdminBPForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_admins')
    else:
        form = AdminBPForm()
    return render(request, 'crear_admin.html', {'form': form})

def listar_admins(request):
    admins = adminbp.objects.all()
    return render(request, 'listar_admins.html', {'admins': admins})

def editar_admin(request, id):
    admin = get_object_or_404(adminbp, id_admin=id)
    if request.method == 'POST':
        form = AdminBPForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('listar_admins')
    else:
        form = AdminBPForm(instance=admin)
    return render(request, 'editar_admin.html', {'form': form})

def eliminar_admin(request, id):
    admin = get_object_or_404(adminbp, id_admin=id)
    if request.method == 'POST':
        admin.delete()
        return redirect('listar_admins')
    return render(request, 'eliminar_admin.html', {'admin': admin})

def logout_view(request):
    logout(request)
    return redirect('login')

#APP MOVIL
@api_view(['GET', 'POST'])
def centros_listado(request):
    if request.method == 'GET':
        centros = centro_donacion.objects.all()
        serializer = CentroDonacionSerializer(centros, many=True)
        return Response({
            "status": "success",
            "count": centros.count(),
            "data": serializer.data
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


    return Response({
        "status": "success",
        "message": "Donación registrada exitosamente.",
        "donacion_id": nueva_donacion.id_donacion,
        "fecha_donacion": nueva_donacion.fecha_donacion.isoformat(),
        "centro": centro.nombre_centro
    }, status=201)

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