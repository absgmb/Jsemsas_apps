from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AmbulanceTariff,AmbulanceDispatch,GPSPoint
from .serializers import TariffSerializer,DispatchSerializer,GPSPointSerializer
from .utils import verify_qr_token
from accounts.models import DriverProfile
from accounts.permissions import AdminOnly,Dispatchers,Drivers
class TariffViewSet(viewsets.ModelViewSet):
 queryset=AmbulanceTariff.objects.all(); serializer_class=TariffSerializer; permission_classes=[AdminOnly]
class DispatchViewSet(viewsets.ModelViewSet):
 queryset=AmbulanceDispatch.objects.select_related("ambulance","assigned_driver","destination_facility","incident_category"); serializer_class=DispatchSerializer; permission_classes=[Dispatchers]
 def get_queryset(self):
  qs=super().get_queryset(); u=self.request.user; return qs if u.role=="SUPER_ADMIN" else qs.filter(ambulance__facility=u.facility)
 @action(detail=True,methods=["post"],permission_classes=[Drivers])
 @transaction.atomic
 def accept(self,request,pk=None):
  d=self.get_object()
  if d.status!=d.Status.PENDING or d.assigned_driver_id!=request.user.id: return Response({"detail":"Dispatch is not available."},status=409)
  profile=request.user.driver_profile
  if profile.status!=DriverProfile.Status.AVAILABLE: return Response({"detail":"Driver is unavailable."},status=409)
  d.status=d.Status.ACCEPTED; d.accepted_at=timezone.now(); d.save(update_fields=["status","accepted_at","updated_at"]); profile.status=DriverProfile.Status.BUSY; profile.save(update_fields=["status"]); return Response(DispatchSerializer(d,context={"request":request}).data)
 @action(detail=True,methods=["post"],permission_classes=[Drivers])
 def reject(self,request,pk=None):
  d=self.get_object()
  if d.assigned_driver_id!=request.user.id or d.status!=d.Status.PENDING: return Response({"detail":"Invalid rejection."},status=409)
  d.status=d.Status.REJECTED; d.rejection_reason=request.data.get("reason","I'm Busy"); d.save(update_fields=["status","rejection_reason","updated_at"]); request.user.driver_profile.status=DriverProfile.Status.AVAILABLE; request.user.driver_profile.save(update_fields=["status"]); return Response({"status":"rejected"})
 @action(detail=True,methods=["post"],permission_classes=[Drivers])
 def gps(self,request,pk=None):
  d=self.get_object(); s=GPSPointSerializer(data={**request.data,"dispatch":d.pk},context={"request":request}); s.is_valid(raise_exception=True); p=s.save(); profile=request.user.driver_profile; profile.last_location=p.location; profile.last_location_at=p.recorded_at; profile.save(update_fields=["last_location","last_location_at"]); return Response(GPSPointSerializer(p).data,status=201)
 @action(detail=True,methods=["post"],permission_classes=[Drivers])
 def reach_incident(self,request,pk=None): return self._reach(request,self.get_object(),self.get_object().caller_location,self.get_object().Status.ARRIVED_INCIDENT)
 @action(detail=True,methods=["post"],permission_classes=[Drivers])
 def reach_facility(self,request,pk=None):
  d=self.get_object()
  if not d.destination_location: return Response({"detail":"Destination coordinates are missing."},status=400)
  return self._reach(request,d,d.destination_location,d.Status.ARRIVED_FACILITY)
 def _reach(self,request,d,target,next_status):
  if d.assigned_driver_id!=request.user.id: return Response({"detail":"Not assigned."},status=403)
  profile=request.user.driver_profile
  if not profile.last_location: return Response({"detail":"No recent GPS position."},status=409)
  distance_obj=DriverProfile.objects.filter(pk=profile.pk).annotate(distance_m=Distance("last_location",target)).values_list("distance_m",flat=True).first()
  distance_m=float(distance_obj.m) if distance_obj is not None else None
  if distance_m is None or distance_m>100: return Response({"detail":f"Too far from target ({distance_m:.1f}m)." if distance_m is not None else "No GPS position."},status=409)
  d.status=next_status; d.save(update_fields=["status","updated_at"]); return Response({"status":next_status,"distance_m":distance_m})
class GPSPointViewSet(viewsets.ReadOnlyModelViewSet):
 queryset=GPSPoint.objects.all(); serializer_class=GPSPointSerializer; permission_classes=[IsAuthenticated]
class VerifyClaimView(APIView):
 permission_classes=[AllowAny]
 def get(self,request):
  token=request.query_params.get("token")
  if not token:return Response({"valid":False},status=400)
  try:
   payload=verify_qr_token(token)
   if payload["type"]!="dispatch":return Response({"valid":False},status=400)
   obj=get_object_or_404(AmbulanceDispatch,pk=payload["id"])
   return Response({"valid":True,"type":"dispatch","unique_code":obj.unique_code,"status":obj.status,"patient_name":obj.patient_name,"amount":str(obj.total_claim_amount)})
  except Exception:return Response({"valid":False},status=400)
