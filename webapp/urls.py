from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^', views.home),
    url(r'^2/', views.home2),
    url(r'^3/', views.home3),
]
