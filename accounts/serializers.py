from rest_framework import serializers
from .models import User,Facility,Ambulance,DriverProfile
class UserSerializer(serializers.ModelSerializer):
 class Meta: model=User; fields=("id","username","first_name","last_name","phone","role","facility")
class FacilitySerializer(serializers.ModelSerializer):
 class Meta: model=Facility; fields="__all__"
class AmbulanceSerializer(serializers.ModelSerializer):
 class Meta: model=Ambulance; fields="__all__"
class DriverProfileSerializer(serializers.ModelSerializer):
 ambulance_id=serializers.CharField(source="user.assigned_ambulance.ambulance_id",read_only=True)
 class Meta: model=DriverProfile; fields=("id","user","status","last_location","last_location_at","ambulance_id"); read_only_fields=("last_location_at",)
class UserCreateSerializer(serializers.ModelSerializer):
 password=serializers.CharField(write_only=True,min_length=12)
 class Meta: model=User; fields=("username","password","first_name","last_name","phone","role","facility")
 def create(self,validated_data): return User.objects.create_user(**validated_data)
