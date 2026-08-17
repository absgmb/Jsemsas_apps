from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

from accounts.models import Ambulance, DriverProfile, Facility, User
from dispatches.models import AmbulanceDispatch
from etc_claims.models import ETCClaim


def staff_required(view):
    return user_passes_test(lambda u: u.is_active and u.is_staff)(view)


@staff_required
def dashboard(request):
    today = timezone.localdate()
    week_start = today - timedelta(days=6)
    dispatches = AmbulanceDispatch.objects.filter(created_at__date__gte=week_start)
    etc_claims = ETCClaim.objects.filter(created_at__date__gte=week_start)
    context = {
        "stats": {
            "users": User.objects.count(),
            "facilities": Facility.objects.filter(is_active=True).count(),
            "ambulances": Ambulance.objects.filter(is_active=True).count(),
            "available_drivers": DriverProfile.objects.filter(status=DriverProfile.Status.AVAILABLE).count(),
            "active_dispatches": AmbulanceDispatch.objects.exclude(status__in=[AmbulanceDispatch.Status.COMPLETED, AmbulanceDispatch.Status.REJECTED]).count(),
            "pending_dispatches": AmbulanceDispatch.objects.filter(status=AmbulanceDispatch.Status.PENDING).count(),
            "week_dispatches": dispatches.count(),
            "week_etc": etc_claims.count(),
            "week_dispatch_value": dispatches.aggregate(total=Sum("total_claim_amount"))["total"] or 0,
            "week_etc_value": etc_claims.aggregate(total=Sum("total_amount"))["total"] or 0,
        },
        "recent_dispatches": AmbulanceDispatch.objects.select_related("ambulance", "assigned_driver", "destination_facility").order_by("-created_at")[:10],
        "recent_claims": ETCClaim.objects.select_related("facility", "created_by").order_by("-created_at")[:10],
        "today": today,
        "week_start": week_start,
    }
    return render(request, "dashboard/index.html", context)
