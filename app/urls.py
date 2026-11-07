from django.urls import path
from . import views

urlpatterns = [
    path('upload/',views.import_excel,name='upload_file'),
    path('payroll/',views.view_data,name='payroll'),
    path('payroll/map/<str:emp_id>/',views.map_data,name='payroll_data'),
]
