from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("accounts", "0001_initial"), ("incidents", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="AmbulanceTariff",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ambulance_type", models.CharField(choices=[("ALS", "ALS"), ("BLS", "BLS"), ("KEKE", "Keke")], max_length=10, unique=True)),
                ("base_rate", models.DecimalField(decimal_places=2, max_digits=12)),
                ("included_km", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ("additional_km_rate", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="AmbulanceDispatch",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("unique_code", models.CharField(editable=False, max_length=140, unique=True)),
                ("caller_name", models.CharField(max_length=160)), ("caller_phone", models.CharField(max_length=40)), ("caller_address", models.TextField(blank=True)),
                ("caller_latitude", models.DecimalField(decimal_places=6, max_digits=9)), ("caller_longitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("patient_name", models.CharField(max_length=160)), ("patient_phone", models.CharField(blank=True, max_length=40)), ("patient_age", models.PositiveIntegerField(blank=True, null=True)),
                ("blood_group", models.CharField(blank=True, max_length=8)), ("patient_address", models.TextField(blank=True)),
                ("ambulance_type", models.CharField(choices=[("ALS", "ALS"), ("BLS", "BLS"), ("KEKE", "Keke")], max_length=10)),
                ("destination_latitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)), ("destination_longitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ("status", models.CharField(choices=[("PENDING", "Pending"), ("ACCEPTED", "Accepted"), ("REJECTED", "Rejected"), ("EN_ROUTE_INCIDENT", "En Route Incident"), ("ARRIVED_INCIDENT", "Arrived Incident"), ("EN_ROUTE_FACILITY", "En Route Facility"), ("ARRIVED_FACILITY", "Arrived Facility"), ("COMPLETED", "Completed")], default="PENDING", max_length=30)),
                ("rejection_reason", models.CharField(blank=True, max_length=255)), ("kilometer_span", models.DecimalField(decimal_places=2, default=0, max_digits=10)), ("total_claim_amount", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("qr_token", models.TextField(blank=True)), ("accepted_at", models.DateTimeField(blank=True, null=True)), ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
                ("ambulance", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="dispatches", to="accounts.ambulance")),
                ("assigned_driver", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="dispatches", to=settings.AUTH_USER_MODEL)),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="created_dispatches", to=settings.AUTH_USER_MODEL)),
                ("destination_facility", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="incoming_dispatches", to="accounts.facility")),
                ("incident_category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="incidents.incidentcategory")),
            ],
            options={"indexes": [models.Index(fields=["status", "created_at"], name="dispatches_status_1b8f2e_idx"), models.Index(fields=["assigned_driver", "status"], name="dispatches_assigne_6b3c4a_idx")]},
        ),
        migrations.CreateModel(
            name="GPSPoint",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("latitude", models.DecimalField(decimal_places=6, max_digits=9)), ("longitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("accuracy_m", models.FloatField(blank=True, null=True)), ("speed_mps", models.FloatField(blank=True, null=True)), ("recorded_at", models.DateTimeField()),
                ("device_id_hash", models.CharField(blank=True, max_length=128)), ("is_suspect", models.BooleanField(default=False)), ("reason", models.CharField(blank=True, max_length=255)),
                ("dispatch", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="gps_points", to="dispatches.ambulancedispatch")),
                ("driver", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={"indexes": [models.Index(fields=["dispatch", "recorded_at"], name="dispatches_dispatc_1df0d0_idx")]},
        ),
    ]
