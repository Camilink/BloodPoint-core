from datetime import date
import logging
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import donanteSerializer, CentroDonacionSerializer
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from bloodpoint_app.models import CustomUser, donante
from .models import CustomUser, representante_org, donante, centro_donacion
from .serializers import CustomUserSerializer, RepresentanteOrgSerializer, DonantePerfilSerializer
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import uuid
from bloodpoint_app import views



logger = logging.getLogger(__name__)

#def home_view(request):
#    return HttpResponse("Welcome to Bloodpoint API")

# NAVEGADOR 
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def signup(request):

    if request.method == 'POST':
        rut = request.POST.get('rut')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        rol = request.POST.get('rol')
        credencial = request.FILES.get('credencial')
        
        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Las contraseñas no coinciden'})
        myuser = CustomUser.objects.create_user(email, password=password1)
        myuser.save()
        
        representante = representante_org.objects.create(
            user=myuser,
            rol=rol,
            nombre=request.POST.get('nombre'),
            rut=rut,
        )
        representante.save()
        return redirect('login.html')        
    else:
        return render(request, 'signup.html')
    return render(request, 'signup.html')

def logout(request):
    pass
    return redirect('login.html')

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

#APACHE SUPERSET
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