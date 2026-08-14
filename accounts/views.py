from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.gis.geos import Point
from .models import User,Facility,Ambulance,DriverProfile
from .serializers import UserSerializer,UserCreateSerializer,FacilitySerializer,AmbulanceSerializer,DriverProfileSerializer
from .permissions import FacilityAdmins,Drivers
class UserViewSet(viewsets.ModelViewSet):
 queryset=User.objects.all().select_related("facility"); permission_classes=[FacilityAdmins]
 def get_serializer_class(self): return UserCreateSerializer if self.action=="create" else UserSerializer
 def get_queryset(self):
  qs=super().get_queryset(); u=self.request.user
  return qs if u.role=="SUPER_ADMIN" else qs.filter(facility=u.facility)
class FacilityViewSet(viewsets.ModelViewSet):
 queryset=Facility.objects.all(); serializer_class=FacilitySerializer; permission_classes=[FacilityAdmins]
class AmbulanceViewSet(viewsets.ModelViewSet):
 queryset=Ambulance.objects.all().select_related("facility","assigned_driver"); serializer_class=AmbulanceSerializer; permission_classes=[FacilityAdmins]
 def get_queryset(self):
  qs=super().get_queryset(); return qs if self.request.user.role=="SUPER_ADMIN" else qs.filter(facility=self.request.user.facility)
class DriverProfileViewSet(viewsets.ModelViewSet):
 queryset=DriverProfile.objects.all().select_related("user"); serializer_class=DriverProfileSerializer; permission_classes=[Drivers]
 @action(detail=True,methods=["post"])
 def location(self,request,pk=None):
  p=self.get_object(); lat=float(request.data["lat"]); lon=float(request.data["lon"]); p.last_location=Point(lon,lat,srid=4326); p.last_location_at=timezone.now(); p.save(update_fields=["last_location","last_location_at"]); return Response({"status":"ok"})
