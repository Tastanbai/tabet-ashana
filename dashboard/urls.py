from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='kitapdb'),
    path('register/', views.register_page, name='register'),
    path('kitapdb', views.kitapdb_view, name='kitapdb'),
    path('apkdb/', views.apkdb, name='apkdb'),
    path('ashanadb/', views.ashanadb, name='ashanadb'),
]
