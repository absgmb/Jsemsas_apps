from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords
from accounts.models import User, Facility, Ambulance
from incidents.models import IncidentCategory
from .utils import build_unique_code


class AmbulanceTariff(models.Model):
    ambulance_type = models.CharField(max_length=10, choices=Ambulance.Types.choices, unique=True)
    base_rate = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    included_km = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    additional_km_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def calculate(self, km):
        return self.base_rate + max(Decimal(str(km)) - self.included_km, Decimal("0")) * self.additional_km_rate


class AmbulanceDispatch(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"
        EN_ROUTE_INCIDENT = "EN_ROUTE_INCIDENT", "En Route Incident"
        ARRIVED_INCIDENT = "ARRIVED_INCIDENT", "Arrived Incident"
        EN_ROUTE_FACILITY = "EN_ROUTE_FACILITY", "En Route Facility"
        ARRIVED_FACILITY = "ARRIVED_FACILITY", "Arrived Facility"
        COMPLETED = "COMPLETED", "Completed"

    unique_code = models.CharField(max_length=140, unique=True, editable=False)
    caller_name = models.CharField(max_length=160)
    caller_phone = models.CharField(max_length=40)
    caller_address = models.TextField(blank=True)
    caller_latitude = models.DecimalField(max_digits=9, decimal_places=6, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    caller_longitude = models.DecimalField(max_digits=9, decimal_places=6, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    patient_name = models.CharField(max_length=160)
    patient_phone = models.CharField(max_length=40, blank=True)
    patient_age = models.PositiveIntegerField(null=True, blank=True)
    blood_group = models.CharField(max_length=8, blank=True)
    patient_address = models.TextField(blank=True)
    incident_category = models.ForeignKey(IncidentCategory, on_delete=models.PROTECT)
    ambulance = models.ForeignKey(Ambulance, on_delete=models.PROTECT, related_name="dispatches")
    ambulance_type = models.CharField(max_length=10, choices=Ambulance.Types.choices)
    assigned_driver = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name="dispatches")
    destination_facility = models.ForeignKey(Facility, null=True, blank=True, on_delete=models.PROTECT, related_name="incoming_dispatches")
    destination_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    destination_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    rejection_reason = models.CharField(max_length=255, blank=True)
    kilometer_span = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_claim_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    qr_token = models.TextField(blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_dispatches")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["assigned_driver", "status"]),
        ]

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = build_unique_code(self.ambulance.ambulance_id)
        super().save(*args, **kwargs)


class GPSPoint(models.Model):
    dispatch = models.ForeignKey(AmbulanceDispatch, on_delete=models.CASCADE, related_name="gps_points")
    driver = models.ForeignKey(User, on_delete=models.PROTECT)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    accuracy_m = models.FloatField(null=True, blank=True)
    speed_mps = models.FloatField(null=True, blank=True)
    recorded_at = models.DateTimeField()
    device_id_hash = models.CharField(max_length=128, blank=True)
    is_suspect = models.BooleanField(default=False)
    reason = models.CharField(max_length=255, blank=True)

    class Meta:
        indexes = [models.Index(fields=["dispatch", "recorded_at"])]
