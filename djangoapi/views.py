from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import JSONParser 
from django.http.response import JsonResponse
from rest_framework import status

from .serializers import DocumentSerializer
from .models import Document
from rest_framework.decorators import api_view
from prefect import Flow, task
from prefect.tasks.prefect import StartFlowRun

class DocumentViewSet(viewsets.ModelViewSet):
  queryset = Document.objects.all().order_by('name')
  serializer_class = DocumentSerializer

@api_view(['POST'])
def workflow(request):

  document = JSONParser().parse(request)
  graph_building = StartFlowRun(
    flow_name="graph_building",
    project_name="sgwfc-gene",
    wait=True
  )
  with Flow("Call Flow") as flow:
    end_flow = graph_building(parameters=dict(gene_filename=document["name"]))
  state = flow.run()
  import pdb; pdb.set_trace()
  return JsonResponse(
    state.result[end_flow].result, status=status.HTTP_201_CREATED)