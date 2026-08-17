from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Ambulance, DriverProfile, Facility, User
from dispatches.models import AmbulanceDispatch, AmbulanceTariff, GPSPoint
from etc_claims.models import ETCClaim, ETCTreatmentItem, NHIATariff
from incidents.models import IncidentCategory


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "first_name", "last_name", "role", "facility", "is_active", "last_login")
    list_filter = ("role", "is_active", "is_staff", "facility")
    search_fields = ("username", "first_name", "last_name", "phone", "email")
    fieldsets = BaseUserAdmin.fieldsets + (("J-SEMSAS", {"fields": ("role", "phone", "facility")}),)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("facility_code", "name", "lga", "state", "phone", "is_active")
    list_filter = ("state", "lga", "is_active")
    search_fields = ("facility_code", "name", "lga")


@admin.register(Ambulance)
class AmbulanceAdmin(admin.ModelAdmin):
    list_display = ("ambulance_id", "plate_number", "type", "facility", "assigned_driver", "is_active")
    list_filter = ("type", "facility", "is_active")
    search_fields = ("ambulance_id", "plate_number", "car_model")


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "last_location_at")
    list_filter = ("status",)
    search_fields = ("user__username", "user__first_name", "user__last_name")


@admin.register(IncidentCategory)
class IncidentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(AmbulanceTariff)
class AmbulanceTariffAdmin(admin.ModelAdmin):
    list_display = ("ambulance_type", "base_rate", "included_km", "additional_km_rate", "is_active")
    list_filter = ("ambulance_type", "is_active")


@admin.register(AmbulanceDispatch)
class AmbulanceDispatchAdmin(admin.ModelAdmin):
    list_display = ("unique_code", "patient_name", "ambulance", "assigned_driver", "status", "total_claim_amount", "created_at")
    list_filter = ("status", "ambulance_type", "created_at")
    search_fields = ("unique_code", "patient_name", "caller_name", "caller_phone")
    readonly_fields = ("unique_code", "qr_token", "created_at", "updated_at", "accepted_at", "completed_at", "kilometer_span", "total_claim_amount")
    date_hierarchy = "created_at"


@admin.register(GPSPoint)
class GPSPointAdmin(admin.ModelAdmin):
    list_display = ("dispatch", "driver", "recorded_at", "accuracy_m", "speed_mps", "is_suspect")
    list_filter = ("is_suspect", "recorded_at")
    search_fields = ("dispatch__unique_code", "driver__username")


@admin.register(NHIATariff)
class NHIATariffAdmin(admin.ModelAdmin):
    list_display = ("nhis_code", "item_description", "category", "unit_price", "is_active", "source_updated_at")
    list_filter = ("category", "is_active")
    search_fields = ("nhis_code", "item_description")


class ETCTreatmentItemInline(admin.TabularInline):
    model = ETCTreatmentItem
    extra = 0
    readonly_fields = ("unit_price", "subtotal")


@admin.register(ETCClaim)
class ETCClaimAdmin(admin.ModelAdmin):
    list_display = ("unique_code", "patient_name", "facility", "status", "total_amount", "created_by", "created_at")
    list_filter = ("status", "facility", "created_at")
    search_fields = ("unique_code", "patient_name", "patient_phone")
    readonly_fields = ("unique_code", "total_amount", "qr_token", "created_at", "updated_at")
    inlines = (ETCTreatmentItemInline,)
    date_hierarchy = "created_at"
