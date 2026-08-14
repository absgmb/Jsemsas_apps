from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import NHIATariff,ETCClaim,ETCTreatmentItem
from .serializers import NHIATariffSerializer,ETCClaimSerializer,ETCTreatmentItemSerializer
from accounts.permissions import Nurses
class NHIATariffViewSet(viewsets.ReadOnlyModelViewSet):
 queryset=NHIATariff.objects.filter(is_active=True).order_by("item_description"); serializer_class=NHIATariffSerializer; permission_classes=[Nurses]; search_fields=("nhis_code","item_description","category")
class ETCClaimViewSet(viewsets.ModelViewSet):
 queryset=ETCClaim.objects.select_related("facility","created_by").prefetch_related("items"); serializer_class=ETCClaimSerializer; permission_classes=[Nurses]
 def get_queryset(self):
  qs=super().get_queryset(); return qs if self.request.user.role=="SUPER_ADMIN" else qs.filter(facility=self.request.user.facility)
 def perform_create(self,serializer): serializer.save(created_by=self.request.user,facility=self.request.user.facility)
 @action(detail=True,methods=["post"])
 def submit(self,request,pk=None):
  c=self.get_object()
  if c.status!="DRAFT":return Response({"detail":"Only drafts can be submitted."},status=409)
  if not c.items.exists():return Response({"detail":"Claim must contain at least one item."},status=400)
  c.status="SUBMITTED"; c.save(update_fields=["status","updated_at"]); return Response(self.get_serializer(c).data)
class ETCTreatmentItemViewSet(viewsets.ModelViewSet):
 queryset=ETCTreatmentItem.objects.all(); serializer_class=ETCTreatmentItemSerializer; permission_classes=[Nurses]
