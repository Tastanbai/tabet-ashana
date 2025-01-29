from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_page, name='register'),
    path('kitapdb', views.kitapdb_view, name='kitapdb'),
    path('apkdb/', views.apkdb, name='apkdb'),
    path('ashanadb/', views.ashanadb, name='ashanadb'),
]
