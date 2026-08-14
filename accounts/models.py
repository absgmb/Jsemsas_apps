from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords
class User(AbstractUser):
 class Roles(models.TextChoices):
  SUPER_ADMIN="SUPER_ADMIN","Super Admin"; FACILITY_ADMIN="FACILITY_ADMIN","Facility Admin"; DISPATCHER="DISPATCHER","Dispatcher"; DRIVER="DRIVER","Driver"; NURSE="NURSE","Nurse"
 role=models.CharField(max_length=30,choices=Roles.choices); phone=models.CharField(max_length=30,blank=True); facility=models.ForeignKey("Facility",null=True,blank=True,on_delete=models.PROTECT,related_name="users"); history=HistoricalRecords()
 def clean(self):
  from django.core.exceptions import ValidationError
  if self.role!=self.Roles.SUPER_ADMIN and not self.facility: raise ValidationError("Non-super-admin users must belong to a facility.")
class Facility(models.Model):
 name=models.CharField(max_length=255); facility_code=models.CharField(max_length=30,unique=True); address=models.TextField(); state=models.CharField(max_length=100,default="Jigawa"); lga=models.CharField(max_length=100); phone=models.CharField(max_length=30,blank=True); email=models.EmailField(blank=True); location=models.PointField(geography=True,null=True,blank=True); is_active=models.BooleanField(default=True); history=HistoricalRecords()
 def __str__(self): return f"{self.facility_code} - {self.name}"
class Ambulance(models.Model):
 class Types(models.TextChoices): ALS="ALS","ALS"; BLS="BLS","BLS"; KEKE="KEKE","Keke"
 ambulance_id=models.CharField(max_length=60,unique=True); plate_number=models.CharField(max_length=30,unique=True); car_model=models.CharField(max_length=120); type=models.CharField(max_length=10,choices=Types.choices); equipment_list=models.JSONField(default=list,blank=True); facility=models.ForeignKey(Facility,on_delete=models.PROTECT,related_name="ambulances"); assigned_driver=models.OneToOneField(User,null=True,blank=True,on_delete=models.SET_NULL,related_name="assigned_ambulance",limit_choices_to={"role":"DRIVER"}); is_active=models.BooleanField(default=True); history=HistoricalRecords()
 def __str__(self): return self.ambulance_id
class DriverProfile(models.Model):
 class Status(models.TextChoices): AVAILABLE="AVAILABLE","Available"; BUSY="BUSY","Busy"; OFF_DUTY="OFF_DUTY","Off Duty"; IN_GARAGE="IN_GARAGE","In Garage"
 user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="driver_profile"); status=models.CharField(max_length=20,choices=Status.choices,default=Status.OFF_DUTY); last_location=models.PointField(geography=True,null=True,blank=True); last_location_at=models.DateTimeField(null=True,blank=True); history=HistoricalRecords()
