from datetime import date
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import donanteSerializer
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from bloodpoint_app.models import CustomUser, donante
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import CustomUserSerializer


logger = logging.getLogger(__name__)

def home_view(request):
    return HttpResponse("Welcome to Bloodpoint API")


from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def ingresar(request):
    rut = request.data.get("rut")
    password = request.data.get("password")

    # Autentica al usuario
    user = authenticate(rut=rut, password=password)

    if user is not None:
        # Inicia sesión
        login(request, user)
        return Response({
            "status": "success",
            "message": "Inicio de sesión exitoso.",
            "user_id": user.id
        }, status=200)
    else:
        return Response({
            "status": "error",
            "message": "Rut o contraseña incorrectos."
        }, status=400)

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

    # Crear usuario en CustomUser
    user = CustomUser.objects.create_user(rut=rut, email=email, password=password)

    # Resto de los datos para crear el objeto donante
    donante_data = {
        "rut": rut,
        "nombre_completo": request.data.get("nombre_completo"),
        "direccion": request.data.get("direccion"),
        "comuna": request.data.get("comuna"),
        "fono": request.data.get("fono"),
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
    # Verifica que el usuario esté autenticado
    if not request.user.is_authenticated:
        return Response({
            "status": "error",
            "message": "Usuario no autenticado."
        }, status=403)

    # Solicitud GET: Obtener perfil
    if request.method == 'GET':
        user = request.user  # Usuario autenticado
        serializer = CustomUserSerializer(user)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=200)

    # Solicitud PUT: Actualizar perfil
    elif request.method == 'PUT':
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)

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