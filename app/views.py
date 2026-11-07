from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from openpyxl import load_workbook
from io import BytesIO
from .serializers import FileUploadSerializer,PayrollSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import FormParser,MultiPartParser
import tablib
from .resource import PayrollResource
from .models import PayrollRecord
from weasyprint import HTML


# Create your views here.

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser]) # Ensures DRF accepts multipart file uploads
def import_excel(request):
    serializer = FileUploadSerializer(data=request.data)
    if serializer.is_valid():
        file_obj = serializer.validated_data['file']
        file_format = serializer.validated_data['file_format']
        
        # Standardize format string (remove dots, convert to lowercase)
        file_format = file_format.replace('.', '').lower()
        
        try:
            data = file_obj.read()
            
            # ONLY decode text-based files (like CSV). DO NOT decode binary files like XLSX.
            if file_format == 'csv':
                data = data.decode('utf-8')
            
            # Load dataset using tablib
            dataset = tablib.Dataset().load(data, format=file_format)
            
            resource = PayrollResource()

            # Step 1: Run dry_run to validate data integrity
            result = resource.import_data(dataset=dataset, dry_run=True)
            
            # Step 2: Check for errors and halt if any exist
            if result.has_errors():
                errors = []
                # django-import-export results contain row-by-row error logs
                for row_idx, row_errors in result.row_errors():
                    for row_error in row_errors:
                        errors.append({
                            "row_number": row_idx,
                            "error_message": str(row_error.error),
                            # Optional: uncomment the next line if you need full stacktrace debugging
                            # "traceback": str(row_error.traceback) 
                        })
                
                # Stop processing and return a 400 Bad Request with the actual error log
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            
            # Step 3: Safe to save since dry_run passed with zero errors
            resource.import_data(dataset, dry_run=False)
            return Response({"message": "Data uploaded successfully"}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"errors": f"Processing failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
@api_view(['GET'])
def view_data(request):
    payroll = PayrollRecord.objects.all()
    serializer = PayrollSerializer(payroll,many=True)
    print(serializer.data)
    
    return Response({"data" : serializer.data},status=200)
    
@api_view(['GET'])
def map_data(request,emp_id):
    payroll_record = PayrollRecord.objects.get(emp_id=emp_id)
    print(payroll_record.payslip_pdf)
    if payroll_record.payslip_pdf != "":
        payroll_record.payslip_pdf.open('rb')
        pdf_file = payroll_record.payslip_pdf.read()
        return HttpResponse(pdf_file,content_type='application/pdf')
    total = (payroll_record.basic + payroll_record.hra + payroll_record.da + payroll_record.att_allowance + payroll_record.wa + payroll_record.incentives)

    payroll_data = render_to_string('salary_slip.html',{'emp' : payroll_record, 'total' : total})
    pdf_file = HTML(string=payroll_data).write_pdf()
    payroll_record.payslip_pdf.save(f"salary_slip_{emp_id}_{payroll_record.month}_{payroll_record.year}.pdf",ContentFile(pdf_file),save=True)

    response = HttpResponse(pdf_file,content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="salary_slip.pdf"'
    return response
    

 
