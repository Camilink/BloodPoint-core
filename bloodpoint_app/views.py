from datetime import date
import logging
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import donanteSerializer
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from bloodpoint_app.models import CustomUser, donante
from .models import CustomUser, representante_org, donante
from .serializers import CustomUserSerializer, RepresentanteOrgSerializer, DonantePerfilSerializer
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import uuid
from bloodpoint_app import views



logger = logging.getLogger(__name__)

#def home_view(request):
#    return HttpResponse("Welcome to Bloodpoint API")

# NAVEGADOR 
def HomePage(request):
    return render(request, 'home.html')

def LoginPage(request):
    return render(request, 'login.html')

def SignupPage(request):
    return render(request, 'signup.html')



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

