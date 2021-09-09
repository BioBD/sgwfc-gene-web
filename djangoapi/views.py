import time
import simplejson
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from djangoapi.serializers import DocumentSerializer
from djangoapi.models import Document
from prefect import Flow, Client
from prefect.tasks.prefect import StartFlowRun
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 


class DocumentViewSet(viewsets.ModelViewSet, LoginRequiredMixin):
  queryset = Document.objects.all().order_by('name')
  serializer_class = DocumentSerializer


@login_required
def tool(request):
    """Função da View para página Home"""
    return render(request, 'front-end/index.html')


@login_required
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
