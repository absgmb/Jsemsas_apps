from rest_framework import serializers
from .models import NHIATariff,ETCClaim,ETCTreatmentItem
class NHIATariffSerializer(serializers.ModelSerializer):
 class Meta: model=NHIATariff; fields="__all__"
class ETCTreatmentItemSerializer(serializers.ModelSerializer):
 class Meta: model=ETCTreatmentItem; fields="__all__"; read_only_fields=("unit_price","subtotal")
class ETCClaimSerializer(serializers.ModelSerializer):
 items=ETCTreatmentItemSerializer(many=True,read_only=True)
 class Meta: model=ETCClaim; fields="__all__"; read_only_fields=("unique_code","total_amount","qr_token","created_by")
