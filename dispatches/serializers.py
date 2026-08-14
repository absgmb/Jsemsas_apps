from django.contrib.gis.geos import Point
from rest_framework import serializers
from .models import AmbulanceTariff,AmbulanceDispatch,GPSPoint
from .utils import build_qr_token
class TariffSerializer(serializers.ModelSerializer):
 class Meta: model=AmbulanceTariff; fields="__all__"
class GPSPointSerializer(serializers.ModelSerializer):
 lat=serializers.FloatField(write_only=True); lon=serializers.FloatField(write_only=True)
 class Meta: model=GPSPoint; fields=("id","dispatch","driver","lat","lon","accuracy_m","speed_mps","recorded_at","is_suspect","reason"); read_only_fields=("driver","is_suspect","reason")
 def create(self,validated):
  lat=validated.pop("lat"); lon=validated.pop("lon"); validated["driver"]=self.context["request"].user; validated["location"]=Point(lon,lat,srid=4326); accuracy=validated.get("accuracy_m"); validated["is_suspect"]=bool(accuracy is not None and accuracy>100); validated["reason"]="Low GPS accuracy" if validated["is_suspect"] else ""; return super().create(validated)
class DispatchSerializer(serializers.ModelSerializer):
 class Meta: model=AmbulanceDispatch; fields="__all__"; read_only_fields=("unique_code","created_by","qr_token","total_claim_amount","kilometer_span")
 def create(self,validated):
  obj=super().create({**validated,"created_by":self.context["request"].user}); obj.qr_token=build_qr_token("dispatch",obj.pk); obj.save(update_fields=["qr_token"]); return obj
class DispatchActionSerializer(serializers.Serializer): reason=serializers.CharField(required=False,allow_blank=True,max_length=255)
