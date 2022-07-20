import time
import os
import uuid
import simplejson
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from djangoapi.serializers import DocumentSerializer
from djangoapi.models import Document
from prefect import Flow, Client
from prefect.tasks.prefect import StartFlowRun
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 
from django.contrib.auth.models import User
import pickle
import networkx
import datetime

PATH_CURRENT = os.getcwd()

# class DocumentViewSet(viewsets.ModelViewSet, LoginRequiredMixin):
#     queryset = Document.objects.all().order_by('name')
#     serializer_class = DocumentSerializer

@login_required
def tool(request):
    """Função da View para página Home"""
    return render(request, 'front-end/index.html')


@login_required
@api_view(['POST'])
def uploadFile(request):
    error = True
    if 'csv' in request.FILES:
        fileCSV = request.FILES.getlist('csv')[0]

        if fileCSV.name.lower().endswith('.csv'):
            try:         
                token = uuid.uuid4().hex[:14]
                name_file = token + 'token_' + fileCSV.name
                path = os.path.join(PATH_CURRENT, 'documents', name_file)

                with open(path, 'wb+') as destination:
                    for chunk in fileCSV.chunks():
                        destination.write(chunk)

                user = User.objects.get(id=request.user.id)
                document = Document(name=name_file, path=path, user=user)
                document.save()

            except Exception:
                return HttpResponse(
                    simplejson.dumps({'error': error, 'message': 'Error saving CSV file.'}),
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content_type="application/json"
                )

            error = False
            return HttpResponse(
                simplejson.dumps({'error': error}),
                status=status.HTTP_200_OK,
                content_type="application/json"
            )

    return HttpResponse(
        simplejson.dumps({'error': error, 'message': 'Invalid input CSV file.'}),
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content_type="application/json"
    )


@login_required
@api_view(['GET'])
def getFilesUser(request):
    user = User.objects.get(id=request.user.id)
    documents = Document.objects.all().filter(user_id=user.id).order_by('-uploaded_at')

    files = []
    for document in documents:
        file = {
            'id':document.id,
            'name': document.name.split('token_')[1],
            'date_upload': document.uploaded_at.strftime('%d/%m/%Y %H:%M:%S')
        }
        files.append(file)

    # breakpoint()

    return HttpResponse(
        simplejson.dumps({'files': files}),
        status=status.HTTP_200_OK,
        content_type="application/json"
    )

@login_required
@api_view(['GET'])
def deleteFileUser(request):
    error = False
    try:
        idFile = int(request.GET["id"])
        Document.objects.filter(id=idFile).delete()   
    except Exception:    
        error=True

    return HttpResponse(                
        simplejson.dumps({'error': error}),
        status=status.HTTP_200_OK,
        content_type="application/json"
    )

@login_required
@api_view(['POST'])
def workflow(request):
    tokenFile = int(request.data.get('tokenFile'))
    pathFile = Document.objects.filter(id=tokenFile).values_list('path', flat=True).first()

    # print(request)
    # document = JSONParser().parse(request)

    '''
    graph_building = StartFlowRun(
        flow_name="graph_building",
        project_name="sgwfc-gene",
        wait=False
    )

    with Flow("Call Flow") as flow:
        end_flow = graph_building(parameters=dict(gene_filename=pathFile))
        # end_flow = graph_building(parameters=dict(gene_filename='/input/base_wgcna.csv'))
    state = flow.run()
    flow_id = state.result[end_flow].result
    client = Client()

    while not client.get_flow_run_info(flow_id).state.is_finished():
        time.sleep(5)
    info = client.get_flow_run_info(flow_id)
    last_task = info.task_runs.pop()
    graph = last_task.state.load_result(last_task.state._result).result
    breakpoint()  
    '''
    g = pickle.load(open('file.pkl','rb'))
    G = networkx.path_graph(g)
    graph = networkx.cytoscape_data(G)

    # bb = networkx.betweenness_centrality(G)
    # networkx.set_node_attributes(G, bb, "betweenness")

    return HttpResponse(
        simplejson.dumps(graph['elements'], ignore_nan=True),
        status=status.HTTP_201_CREATED,
        content_type="application/json"
    )

    # return HttpResponse(
    #     simplejson.dumps(graph['elements'], ignore_nan=True),    
    #     status=status.HTTP_201_CREATED,
    #     content_type="application/json"
    # )
