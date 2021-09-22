import time
import os
import re
import uuid
from django.views.decorators.csrf import csrf_exempt
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
from django.contrib.auth.models import User

PATH_CURRENT = os.getcwd()

'''class DocumentViewSet(viewsets.ModelViewSet, LoginRequiredMixin):
  queryset = Document.objects.all().order_by('name')
  serializer_class = DocumentSerializer'''

@login_required
def tool(request):
    """Função da View para página Home"""
    return render(request, 'front-end/index.html')

@login_required
@api_view(['POST'])
def uploadFile(request):

  error = True
  if 'csv' in request.FILES:

        document = request.FILES.getlist('csv')[0]

        try:         
            cont = 1
            columnsValidation = ["SUID","COEXPRESSION","COOCCURRENCE","DATABASES","EXPERIMENTS","FUSION","INTERACTION","INTERSPECIES","NAME","NEIGHBORHOOD","SCORE","SELECTED","SHARED INTERACTION","SHARED NAME","TEXTMINING"]
            chunk = document.read(200) 
            words = str(chunk).split(',')
            for word in words:
                word =  re.sub(r'\b[a-zA-Z]\b', '', word)
                word =  re.sub(r'[0-9]', '', word)
                word = word.replace("\'",'').replace('\"','').replace('\\','')
                if word.upper() in columnsValidation:
                  cont = cont+1
             
            if cont != 16:

              return HttpResponse(
                simplejson.dumps({'error': error, 'message': 'There are invalid or missing columns in the CSV file.'}),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content_type="application/json"
              )

            else:

              token = uuid.uuid4().hex[:14]
              name_file = token+'token_'+document.name
              path = os.path.join(PATH_CURRENT, 'documents', name_file)

              with open(path, 'wb+') as destination:
                  for chunk in document.chunks():
                     destination.write(chunk)                     

        except Exception:

            return HttpResponse(
                simplejson.dumps({'error': error, 'message':'Error saving CSV file.'}),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content_type="application/json"
            )

        user = User.objects.get(id=request.user.id)        
        document = Document(name=name_file, path=path, user=user)
        document.save()

        # name = models.CharField(max_length=80)
        #path = models.CharField(max_length=200)  
        #uploaded_at = models.DateTimeField(auto_now_add=True)
        #user = models.ForeignKey(User)
        #document.name = name_file

        error = False
        return HttpResponse(
                  simplejson.dumps({'error': error}),
                  status=status.HTTP_200_OK,
                  content_type="application/json"
        )

  else:
        return HttpResponse(
                simplejson.dumps({'error': error, 'message':'Invalid input CSV file.'}),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content_type="application/json"
        )

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
