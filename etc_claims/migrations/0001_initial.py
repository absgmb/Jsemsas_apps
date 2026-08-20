from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("accounts", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="NHIATariff",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nhis_code", models.CharField(max_length=80, unique=True)), ("item_description", models.CharField(max_length=500)),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=14)),
                ("category", models.CharField(choices=[("DRUGS", "Drugs"), ("BED", "Bed"), ("NURSING", "Nursing Care"), ("DIAGNOSTICS", "Diagnostics"), ("PROCEDURE", "Procedure")], max_length=20)),
                ("is_active", models.BooleanField(default=True)), ("source_updated_at", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ETCClaim",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("unique_code", models.CharField(editable=False, max_length=140, unique=True)), ("patient_name", models.CharField(max_length=160)),
                ("patient_phone", models.CharField(blank=True, max_length=40)), ("patient_age", models.PositiveIntegerField(blank=True, null=True)),
                ("case_category", models.CharField(max_length=160)), ("total_amount", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("live_photo_evidence", models.ImageField(blank=True, null=True, upload_to="etc/evidence/%Y/%m/")),
                ("status", models.CharField(choices=[("DRAFT", "Draft"), ("SUBMITTED", "Submitted"), ("UNDER_REVIEW", "Under Review"), ("APPROVED", "Approved"), ("DISBURSED", "Disbursed"), ("REJECTED", "Rejected")], default="DRAFT", max_length=20)),
                ("qr_token", models.TextField(blank=True)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="etc_claims", to=settings.AUTH_USER_MODEL)),
                ("facility", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="etc_claims", to="accounts.facility")),
            ],
        ),
        migrations.CreateModel(
            name="ETCTreatmentItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)), ("unit_price", models.DecimalField(decimal_places=2, editable=False, max_digits=14)), ("subtotal", models.DecimalField(decimal_places=2, editable=False, max_digits=14)),
                ("claim", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="etc_claims.etcclaim")),
                ("tariff", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="etc_claims.nhiatariff")),
            ],
        ),
    ]
