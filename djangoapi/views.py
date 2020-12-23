import time
import simplejson
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import JSONParser 
from django.http import HttpResponse
from rest_framework import status

from .serializers import DocumentSerializer
from .models import Document
from rest_framework.decorators import api_view
from prefect import Flow, task, Client
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
    wait=False
  )
  with Flow("Call Flow") as flow:
    end_flow = graph_building(parameters=dict(gene_filename=document["name"]))
  state = flow.run()
  flow_id = state.result[end_flow].result
  client = Client()

  while not client.get_flow_run_info(flow_id).state.is_finished():
      time.sleep(5)
  info = client.get_flow_run_info(flow_id)
  last_task = info.task_runs.pop()
  graph = last_task.state.load_result(last_task.state._result).result
  return HttpResponse(
    simplejson.dumps(graph["elements"], ignore_nan=True),
    status=status.HTTP_201_CREATED,
    content_type="application/json"
  )