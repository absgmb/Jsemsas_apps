from math import radians, sin, cos, asin, sqrt
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AmbulanceTariff, AmbulanceDispatch, GPSPoint
from .serializers import TariffSerializer, DispatchSerializer, GPSPointSerializer
from .utils import verify_qr_token
from accounts.models import DriverProfile
from accounts.permissions import AdminOnly, Dispatchers, Drivers


def haversine_m(lat1, lon1, lat2, lon2):
    r = 6371000.0
    p1, p2 = radians(float(lat1)), radians(float(lat2))
    dp = radians(float(lat2) - float(lat1))
    dl = radians(float(lon2) - float(lon1))
    a = sin(dp / 2) ** 2 + cos(p1) * cos(p2) * sin(dl / 2) ** 2
    return 2 * r * asin(sqrt(a))


class TariffViewSet(viewsets.ModelViewSet):
    queryset = AmbulanceTariff.objects.all()
    serializer_class = TariffSerializer
    permission_classes = [AdminOnly]


class DispatchViewSet(viewsets.ModelViewSet):
    queryset = AmbulanceDispatch.objects.select_related("ambulance", "assigned_driver", "destination_facility", "incident_category")
    serializer_class = DispatchSerializer
    permission_classes = [Dispatchers]

    def get_queryset(self):
        qs = super().get_queryset()
        u = self.request.user
        return qs if u.role == "SUPER_ADMIN" else qs.filter(ambulance__facility=u.facility)

    @action(detail=True, methods=["post"], permission_classes=[Drivers])
    @transaction.atomic
    def accept(self, request, pk=None):
        d = self.get_object()
        if d.status != d.Status.PENDING or d.assigned_driver_id != request.user.id:
            return Response({"detail": "Dispatch is not available."}, status=409)
        profile = request.user.driver_profile
        if profile.status != DriverProfile.Status.AVAILABLE:
            return Response({"detail": "Driver is unavailable."}, status=409)
        d.status = d.Status.ACCEPTED
        d.accepted_at = timezone.now()
        d.save(update_fields=["status", "accepted_at", "updated_at"])
        profile.status = DriverProfile.Status.BUSY
        profile.save(update_fields=["status"])
        return Response(DispatchSerializer(d, context={"request": request}).data)

    @action(detail=True, methods=["post"], permission_classes=[Drivers])
    def reject(self, request, pk=None):
        d = self.get_object()
        if d.assigned_driver_id != request.user.id or d.status != d.Status.PENDING:
            return Response({"detail": "Invalid rejection."}, status=409)
        d.status = d.Status.REJECTED
        d.rejection_reason = request.data.get("reason", "I'm Busy")
        d.save(update_fields=["status", "rejection_reason", "updated_at"])
        request.user.driver_profile.status = DriverProfile.Status.AVAILABLE
        request.user.driver_profile.save(update_fields=["status"])
        return Response({"status": "rejected"})

    @action(detail=True, methods=["post"], permission_classes=[Drivers])
    def gps(self, request, pk=None):
        d = self.get_object()
        s = GPSPointSerializer(data={**request.data, "dispatch": d.pk}, context={"request": request})
        s.is_valid(raise_exception=True)
        p = s.save()
        profile = request.user.driver_profile
        profile.last_latitude = p.latitude
        profile.last_longitude = p.longitude
        profile.last_location_at = p.recorded_at
        profile.save(update_fields=["last_latitude", "last_longitude", "last_location_at"])
        return Response(GPSPointSerializer(p).data, status=201)

    @action(detail=True, methods=["post"], permission_classes=[Drivers])
    def reach_incident(self, request, pk=None):
        d = self.get_object()
        return self._reach(request, d, d.caller_latitude, d.caller_longitude, d.Status.ARRIVED_INCIDENT)

    @action(detail=True, methods=["post"], permission_classes=[Drivers])
    def reach_facility(self, request, pk=None):
        d = self.get_object()
        if d.destination_latitude is None or d.destination_longitude is None:
            return Response({"detail": "Destination coordinates are missing."}, status=400)
        return self._reach(request, d, d.destination_latitude, d.destination_longitude, d.Status.ARRIVED_FACILITY)

    def _reach(self, request, d, target_lat, target_lon, next_status):
        if d.assigned_driver_id != request.user.id:
            return Response({"detail": "Not assigned."}, status=403)
        profile = request.user.driver_profile
        if profile.last_latitude is None or profile.last_longitude is None:
            return Response({"detail": "No recent GPS position."}, status=409)
        distance_m = haversine_m(profile.last_latitude, profile.last_longitude, target_lat, target_lon)
        if distance_m > 100:
            return Response({"detail": f"Too far from target ({distance_m:.1f}m)."}, status=409)
        d.status = next_status
        d.save(update_fields=["status", "updated_at"])
        return Response({"status": next_status, "distance_m": round(distance_m, 2)})


class GPSPointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GPSPoint.objects.all()
    serializer_class = GPSPointSerializer
    permission_classes = [IsAuthenticated]


class VerifyClaimView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response({"valid": False}, status=400)
        try:
            payload = verify_qr_token(token)
            if payload["type"] != "dispatch":
                return Response({"valid": False}, status=400)
            obj = get_object_or_404(AmbulanceDispatch, pk=payload["id"])
            return Response({"valid": True, "type": "dispatch", "unique_code": obj.unique_code, "status": obj.status, "patient_name": obj.patient_name, "amount": str(obj.total_claim_amount)})
        except Exception:
            return Response({"valid": False}, status=400)
