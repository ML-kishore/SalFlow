from rest_framework import serializers
from .models import PayrollRecord


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    file_format = serializers.ChoiceField(choices=['csv','xlsx','json'],default='xlsx')

    
class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model=PayrollRecord
        fields = '__all__'
