from rest_framework import serializers
from .models import *

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class ReportPerDaySerializer(serializers.Serializer):
    day = serializers.CharField()
    available = serializers.CharField()

class MoneySerializer(serializers.Serializer):
    address = serializers.CharField()
    money_come = serializers.CharField()
    money_go = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserRatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = "user.username")
    class Meta:
        model = UserRating
        fields = "__all__"
