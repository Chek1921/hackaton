from rest_framework import serializers
from .models import *

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class RatingSerializer(serializers.Serializer):
    rating = serializers.CharField()
    reportId = serializers.CharField()


