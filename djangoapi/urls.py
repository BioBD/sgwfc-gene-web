from django.urls import include, path
from rest_framework import routers
from djangoapi.views import  workflow, tool, uploadFile

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('uploadFile/', uploadFile),
    path('tool/', tool, name='front-end'),
    path('workflow/', workflow),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]