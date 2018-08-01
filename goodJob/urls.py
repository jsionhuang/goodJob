"""goodJob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from jobweb.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',index,name='index'),
    path('search/',search,name='search'),
    path('fsearch1/',fsearch1),
    path('fsearch2/',fsearch2),
    path('classfy/',classfy,name='classfy'),
    path('personal/',personal,name='personal'),
    path('emaliExit/',emaliExit),
    path('login/',login,name='login'),
    path('register/',register,),
    path('logout/',logout,),
    path('collect/',collect),
    path('escollect/',escollect),
    path('chart/',chart,name='chart'),
    path('news/',news,name='news'),

]
