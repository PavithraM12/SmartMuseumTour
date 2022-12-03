from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_html),
    path('ScanQRCode/', views.open_camera),
]