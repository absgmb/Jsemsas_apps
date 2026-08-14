from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from simple_history.models import HistoricalRecords
from accounts.models import Facility,User
from dispatches.utils import build_etc_code,build_qr_token
class NHIATariff(models.Model):
 class Categories(models.TextChoices): DRUGS="DRUGS","Drugs"; BED="BED","Bed"; NURSING="NURSING","Nursing Care"; DIAGNOSTICS="DIAGNOSTICS","Diagnostics"; PROCEDURE="PROCEDURE","Procedure"
 nhis_code=models.CharField(max_length=80,unique=True); item_description=models.CharField(max_length=500); unit_price=models.DecimalField(max_digits=14,decimal_places=2,validators=[MinValueValidator(0)]); category=models.CharField(max_length=20,choices=Categories.choices); is_active=models.BooleanField(default=True); source_updated_at=models.DateTimeField(null=True,blank=True); history=HistoricalRecords()
class ETCClaim(models.Model):
 class Status(models.TextChoices): DRAFT="DRAFT","Draft"; SUBMITTED="SUBMITTED","Submitted"; UNDER_REVIEW="UNDER_REVIEW","Under Review"; APPROVED="APPROVED","Approved"; DISBURSED="DISBURSED","Disbursed"; REJECTED="REJECTED","Rejected"
 unique_code=models.CharField(max_length=140,unique=True,editable=False); facility=models.ForeignKey(Facility,on_delete=models.PROTECT,related_name="etc_claims"); patient_name=models.CharField(max_length=160); patient_phone=models.CharField(max_length=40,blank=True); patient_age=models.PositiveIntegerField(null=True,blank=True); case_category=models.CharField(max_length=160); total_amount=models.DecimalField(max_digits=14,decimal_places=2,default=0); live_photo_evidence=models.ImageField(upload_to="etc/evidence/%Y/%m/",null=True,blank=True); created_by=models.ForeignKey(User,on_delete=models.PROTECT,related_name="etc_claims"); status=models.CharField(max_length=20,choices=Status.choices,default=Status.DRAFT); qr_token=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True); history=HistoricalRecords()
 def save(self,*args,**kwargs):
  new=not self.pk
  if not self.unique_code:self.unique_code=build_etc_code(self.facility.facility_code)
  super().save(*args,**kwargs)
  if new and not self.qr_token:self.qr_token=build_qr_token("etc",self.pk); super().save(update_fields=["qr_token"])
class ETCTreatmentItem(models.Model):
 claim=models.ForeignKey(ETCClaim,on_delete=models.CASCADE,related_name="items"); tariff=models.ForeignKey(NHIATariff,on_delete=models.PROTECT); quantity=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(Decimal("0.01"))]); unit_price=models.DecimalField(max_digits=14,decimal_places=2,editable=False); subtotal=models.DecimalField(max_digits=14,decimal_places=2,editable=False); history=HistoricalRecords()
 def save(self,*args,**kwargs):
  self.unit_price=self.tariff.unit_price; self.subtotal=(self.quantity*self.unit_price).quantize(Decimal("0.01")); super().save(*args,**kwargs); total=sum((x.subtotal for x in self.claim.items.all()),Decimal("0.00")); ETCClaim.objects.filter(pk=self.claim_id).update(total_amount=total)
