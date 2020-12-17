from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import JSONParser 
from django.http.response import JsonResponse
from rest_framework import status

from .serializers import DocumentSerializer
from .models import Document
from rest_framework.decorators import api_view


class DocumentViewSet(viewsets.ModelViewSet):
  queryset = Document.objects.all().order_by('name')
  serializer_class = DocumentSerializer

@api_view(['POST'])
def workflow(request):
  # breakpoint()
  documentData = JSONParser().parse(request)

  print(documentData)
    
  return JsonResponse({"name": "Documento1"}, status=status.HTTP_201_CREATED)