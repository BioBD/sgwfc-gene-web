"""sgwf_gene URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin, auth
from django.views.generic import TemplateView
from django.urls import path, include

from sgwf_gene.auth.views import UserLoginView, PasswordChangeView, createUserView, userCreatedView
from sgwf_gene.auth.forms import UserLoginForm, CustomPasswordResetForm, CustomPasswordChangeForm

admin.site.site_title = 'SGWF Gene'
admin.site.site_header = 'Administração SGWF Gene'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tool/', TemplateView.as_view(template_name='front-end/index.html'), name='front-end'),
    path('', include('home.urls')),
    path('api/', include('djangoapi.urls')),

    path('accounts/login/', UserLoginView.as_view(redirect_authenticated_user=True, authentication_form=UserLoginForm), name='login'),
    path('accounts/password_reset/', auth.views.PasswordResetView.as_view(form_class=CustomPasswordResetForm), name='password_reset'),
    path('accounts/password_change/', PasswordChangeView.as_view(form_class=CustomPasswordChangeForm), name='password_change'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/new/', createUserView, name='user_create'),
    path('accounts/new/done/', userCreatedView, name='user_created')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

