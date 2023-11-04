from django import views
from django.contrib import admin
from django.urls import path
from project.settings import BASE_DIR
from . import views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('',views.home, name="home"),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/',views.signout, name='signout'),
    path('main/',views.main, name='main'),
    path('upload/', views.upload_images, name='upload_images'),
    path('generate_certificate/', views.generate_certificate, name='generate_certificate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('table/', views.table, name='table'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
