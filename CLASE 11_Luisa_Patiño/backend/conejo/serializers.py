
from rest_framework import serializers
from .models import Conejo

class ConejoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conejo
        fields = '__all__'
