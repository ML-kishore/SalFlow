from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from openpyxl import load_workbook
from io import BytesIO
from .serializers import FileUploadSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view


# Create your views here.

@api_view(['POST'])
def fileuploadapi(request):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer = FileUploadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    excel_file = serializer.validated_data['file']
    workbook = load_workbook(filename=BytesIO(excel_file.read()),data_only=True)
    sheet = workbook.active
    rows = list(sheet.iter_rows(values_only=True))

    headers = rows[0]
    employees = []
    for row in rows[1:]:
        employee = dict(zip(headers,row))
        employees.append(employee)

    return Response({"message" : "uploaded","employees" : employees},status=200)


