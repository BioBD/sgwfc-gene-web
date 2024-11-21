import time
import os
import uuid
import requests
import simplejson
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# from djangoapi.serializers import DocumentSerializer
from djangoapi.models import Document, Result
from prefect import Flow, Client
from prefect.tasks.prefect import StartFlowRun
from rest_framework import status  # , viewsets
from rest_framework.decorators import api_view
# from rest_framework.parsers import JSONParser 
from django.contrib.auth.models import User
from zipfile import ZipFile
import json
# import pickle
# import networkx
# import datetime

# directs the path to /home/

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
        fileCSV = request.FILES['csv']
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
            'date_upload': document.uploaded_at.strftime('%d/%m/%Y %H:%M:%S'),
            'has_result': bool(document.result_set.all())
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
@api_view(['GET'])
def downloadResult(request):
    file_id = int(request.GET.get('id'))
    results = Result.objects.filter(document_id=file_id).all()

    if not results:
        return HttpResponseNotFound()

    # cria arquivos separados para cada resultado
    file_paths = []
    for (index, result) in enumerate(results):
        path = os.path.join(PATH_CURRENT, 'results', f'result_{file_id}_{index}.cyjs')
        with open(path, 'w') as destination:
            destination.write(result.result_json)
        file_paths.append(path)

    folder = PATH_CURRENT + '/results/'
    files = os.listdir(folder)

    # cria um zip dos arquivos e remove os arquivos criados
    zip_path = os.path.join(PATH_CURRENT, 'results', f'result_{file_id}.zip')
    zip_file = ZipFile(zip_path, 'w')

    for file in files:
        print( file)
        file_full_path = os.path.join(folder, file)
        zip_file.write(filename=file_full_path, arcname=file)
        os.remove(file_full_path)
    zip_file.close()

    if os.path.exists(zip_path):
        with open(zip_path, 'rb') as rp:
            response = HttpResponse(rp.read())
            response['Content-Type'] = 'application/x-zip-compressed'
            response['Content-Disposition'] = 'attachment; filename=result_' + str(file_id) + '.zip'
        os.remove(zip_path)
        return response
    return HttpResponseServerError()




@login_required
@api_view(['POST'])
def workflow(request):

    file_id = int(request.data.get('id'))
    file = Document.objects.filter(id=file_id).first()
    

    # Define the FastAPI endpoint URL
    url = "http://0.0.0.0:5000/upload-file/"
    
    # Open the file and send it via POST request
    with open(file.path, 'rb') as f:
        response = requests.post(url, files={"file": f}, timeout=300)

    # Check if the response from FastAPI is successful
    if response.status_code == 200:
        # Get the result from the Prefect workflow
        result_data = response.json()

        # removes results from previous runs
        Result.objects.filter(document_id=file_id).delete()
        
        # salva o resultado no banco como JSON
        for graph_dict in result_data:
            result = Result(
                result_json = json.dumps(graph_dict),
                document=file
            )
            result.save()

        return HttpResponse(
            simplejson.dumps(result_data),
            status=status.HTTP_200_OK,
            content_type="application/json"
        )
    else:
        return HttpResponse(
            simplejson.dumps({"error": "Failed to process the file"}),
            status=response.status_code,
            content_type="application/json"
        )




# @login_required
# @api_view(['POST'])
# def workflow_old(request):
    
#     # obtém o arquivo pelo id
#     file_id = int(request.data.get('id'))
#     file = Document.objects.filter(id=file_id).first()
#     print(file_id)
#     # print(request)
#     # document = JSONParser().parse(request)

#     # inicializa o workflow
#     graph_building = StartFlowRun(
#         flow_name="graph_building",
#         project_name="sgwfc-gene",
#         wait=False
#     )
    
#     with Flow("Call Flow") as flow:
#         end_flow = graph_building(parameters=dict(gene_filename=file.name))
#         # end_flow = graph_building(parameters=dict(gene_filename='/input/base_wgcna.csv'))

#     # executa o workflow
#     state = flow.run()
    
#     flow_id = state.result[end_flow].result
#     client = Client()

#     # espera o workflow terminar
#     while not client.get_flow_run_info(flow_id).state.is_finished():
#         time.sleep(5)
    
#     # obtém o resultado da execução do workflow
#     info = client.get_flow_run_info(flow_id)
#     last_task = info.task_runs.pop()
#     cyto_graph_dicts = last_task.state.load_result(last_task.state._result).result

#     if not cyto_graph_dicts:
#         return HttpResponseServerError()

    
#     # salva o resultado no banco como JSON
#     for graph_dict in cyto_graph_dicts:
#         result = Result(
#             result_json = json.dumps(graph_dict),
#             document=file
#         )
#         result.save()

#     # retorna uma resposta indicando que o resultado está disponível
#     return HttpResponse(
#         simplejson.dumps({}),
#         status=status.HTTP_201_CREATED,
#         content_type="application/json"
#     )

#     # g = pickle.load(open('file.pkl','rb'))
#     # G = networkx.path_graph(g)
#     # graph = networkx.cytoscape_data(G)

#     # bb = networkx.betweenness_centrality(G)
#     # networkx.set_node_attributes(G, bb, "betweenness")

#     # return HttpResponse(
#     #     simplejson.dumps(graph['elements'], ignore_nan=True),    
#     #     status=status.HTTP_201_CREATED,
#     #     content_type="application/json"
#     # )