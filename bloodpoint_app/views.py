from datetime import date
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import donante
from .serializers import donanteSerializer
from django.shortcuts import redirect
from django.http import HttpResponse


logger = logging.getLogger(__name__)

def home_view(request):
    return HttpResponse("Welcome to Bloodpoint")


    
@api_view(['GET', 'POST'])
def donantes_listado(request):

    if request.method == 'GET':
        print("DEBUG: Entering donantes_listado view")  # Debug line
        
        donantes = donante.objects.all()
        print("DEBUG: Queryset:", donantes)  # Debug queryset
        print("DEBUG: SQL Query:", str(donantes.query))  # Show raw SQL
        
        serializer = donanteSerializer(donantes, many=True)
        print("DEBUG: Serialized data:", serializer.data)  # Debug serialization
        
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