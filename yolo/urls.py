from django.urls import path

from . import views

urlpatterns = [
    path('',views.test,name='objectdetection'),
    path('login/',views.login,name='login'),
    path('download/<str:image>',views.download,name='download_image')
]