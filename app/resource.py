# resources.py
from import_export import resources
from import_export.fields import Field
from .models import PayrollRecord

class PayrollResource(resources.ModelResource):
    # 1. Maintain the explicit field declaration
    gross = Field(attribute='gross', column_name='gross')

    class Meta:
        model = PayrollRecord
        
