from django.urls import include, path
from rest_framework import routers
from djangoapi.views import DocumentViewSet, workflow, tool

router = routers.DefaultRouter()
router.register(r'document', DocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('fileupload/', views.fileUpload),
    path('tool/', tool, name='front-end'),
    path('workflow/', workflow),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]