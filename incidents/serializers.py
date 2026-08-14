from rest_framework import serializers
from .models import IncidentCategory
class IncidentCategorySerializer(serializers.ModelSerializer):
 class Meta: model=IncidentCategory; fields="__all__"
