"""suarezhermanos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import re_path as url
from django.conf import settings
from django.views.static import serve

from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView,logout_then_login
from django.contrib.auth.decorators import login_required
from fiambres.views import Inicio, InicioSistema
from django.conf import settings
from django.conf.urls.static import static
from usuarios.views import Login
from fiambres.views import add_product,remove_product,decrement_product,clean_product,listado_productos


urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('usuarios/',include(('usuarios.urls', 'usuarios'))),
    path('fiambres/',include(('fiambres.urls','fiambres'))),
    path('add_product/<int:product_id>/',add_product, name = "add_product"),
    path('remove_product/<int:product_id>/',remove_product, name = "remove_product"),
    path('decrement_product/<int:product_id>/',decrement_product, name = "decrement_product"),
    path('clean_product/',clean_product, name = "clean_product"),
    path('',Inicio.as_view(), name = 'index'),
    path('home',login_required(listado_productos), name = 'home'),
    path('accounts/login/', Login.as_view(),{'template_name':'login.html'}, name = 'login'),
    path ('logout/', logout_then_login, name = 'logout')
    ]

# path('cart/',include(('cart.urls','cart'))),