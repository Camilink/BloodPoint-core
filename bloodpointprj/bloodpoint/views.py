from django.http import JsonResponse
from .models import donante
from .serializers import donanteSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def donantes_listado(request, format=None):
    if request.method == 'GET':
        donantes = donante.objects.all()
        serializer = donanteSerializer(donantes, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = donanteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def donante_detail(request, id, format=None):
    try:
        donante_instance = donante.objects.get(pk=id)
    except donante.DoesNotExist:
        return Response({'error': 'Donante not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = donanteSerializer(donante_instance)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = donanteSerializer(donante_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        donante_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  