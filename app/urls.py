from django.urls import path
from . import views

urlpatterns = [
    path('upload/',views.fileuploadapi,name='upload_file')
]
