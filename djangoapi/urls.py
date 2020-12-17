from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'document', views.DocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('fileupload/', views.fileUpload),
    path('workflow/', views.workflow),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]