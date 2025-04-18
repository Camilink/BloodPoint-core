from datetime import date
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import donante
from .serializers import donanteSerializer, userDonanteSerializer
from django.shortcuts import redirect
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)

def home_view(request):
    return HttpResponse("Welcome to Bloodpoint API")

from django.contrib.auth import authenticate

@api_view(['POST'])
def login(request):
    serializer = userDonanteSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        contrasena = serializer.validated_data['contrasena']
        user = authenticate(email=email, password=contrasena)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "status": "success",
                "token": token.key,
                "user": {
                    "email": user.email,
                    "id": user.id_donante
                }
            })
        else:
            return Response({
                "status": "error",
                "message": "Credenciales inválidas"
            }, status=status.HTTP_401_UNAUTHORIZED)

    return Response({
        "status": "error",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register(request):
    serializer = donanteSerializer(data=request.data)
    if serializer.is_valid():
        # Crear el usuario con la contraseña hasheada
        donante_data = serializer.validated_data
        donante_data['contrasena'] = make_password(donante_data['contrasena'])
        
        donante_obj = donante.objects.create(**donante_data)
        
        # Crear el token para el nuevo usuario
        token, _ = Token.objects.get_or_create(user=donante_obj)
        
        return Response({
            "status": "created",
            "data": serializer.data,
            "token": token.key,
            "user": donante_obj.email
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        "status": "error",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def profile(request):

    return Response({})


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