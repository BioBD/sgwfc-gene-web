import time
import os
import uuid
import requests
import simplejson
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError, FileResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# from djangoapi.serializers import DocumentSerializer
from djangoapi.models import Document, Result
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
    results = Result.objects.filter(document_id=file_id).first()

    zip_path = results.path

    
    if os.path.exists(zip_path):
        with open(zip_path, 'rb') as rp:
            response = HttpResponse(rp.read())
            response['Content-Type'] = 'application/x-zip-compressed'
            response['Content-Disposition'] = 'attachment; filename=result_' + str(file_id) + '.zip'
            return response
    return HttpResponseServerError()





@login_required
@api_view(['POST'])
def workflow(request):

    input_id = int(request.data.get('id'))
    input_file = Document.objects.filter(id=input_id).first()
    

    # Define the FastAPI endpoint URL
    base_url = "http://0.0.0.0:5000"
    upload_url = f"{base_url}/upload-file/"
    download_url = f"{base_url}/download-results/"
    
    print("workflow")

    # Open the file and send it via POST request
    with open(input_file.path, 'rb') as f:
        response = requests.post(upload_url, files={"file": f}, timeout=300)

    # Check if the response from FastAPI is successful
    if response.status_code == 200:
        # Get the result from the Prefect workflow
        resp_data = response.json()
        # removes results from previous runs
        Result.objects.filter(document_id=input_id).delete()

        print(resp_data)        

        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            project_zip_path = f"results/results_{input_id}.zip"
            with open(project_zip_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1 MB chunks
                    file.write(chunk)

                result = Result(
                    result_json = json.dumps({}),
                    document=input_file,
                    path=project_zip_path
                )
                result.save()

            return JsonResponse({"message": "File downloaded successfully", "zip_path": project_zip_path})
        else:
            return JsonResponse({"error": "Failed to download file"}, status=response.status_code)
    else:
        return HttpResponse(
            simplejson.dumps({"error": "Failed to process the file"}),
            status=response.status_code,
            content_type="application/json"
        )




# @login_required
# @api_view(['GET'])
# def downloadResult_old(request):
#     file_id = int(request.GET.get('id'))
#     results = Result.objects.filter(document_id=file_id).all()

#     if not results:
#         return HttpResponseNotFound()

#     # cria arquivos separados para cada resultado
#     file_paths = []
#     for (index, result) in enumerate(results):
#         path = os.path.join(PATH_CURRENT, 'results', f'result_{file_id}_{index}.cyjs')
#         with open(path, 'w') as destination:
#             destination.write(result.result_json)
#         file_paths.append(path)

#     folder = PATH_CURRENT + '/results/'
#     files = os.listdir(folder)
    
#     # cria um zip dos arquivos e remove os arquivos criados
#     zip_path = os.path.join(PATH_CURRENT, 'results', f'result_{file_id}.zip')
#     zip_file = ZipFile(zip_path, 'w')

#     for file in files:
#         print( file)
#         file_full_path = os.path.join(folder, file)
#         zip_file.write(filename=file_full_path, arcname=file)
#         os.remove(file_full_path)
#     zip_file.close()

#     if os.path.exists(zip_path):
#         with open(zip_path, 'rb') as rp:
#             response = HttpResponse(rp.read())
#             response['Content-Type'] = 'application/x-zip-compressed'
#             response['Content-Disposition'] = 'attachment; filename=result_' + str(file_id) + '.zip'
#         os.remove(zip_path)
#         return response
#     return HttpResponseServerError()



