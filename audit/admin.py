from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from accounts.models import User,Facility,Ambulance,DriverProfile
from incidents.models import IncidentCategory
from dispatches.models import AmbulanceTariff,AmbulanceDispatch,GPSPoint
from etc_claims.models import NHIATariff,ETCClaim,ETCTreatmentItem
for model in [User,Facility,Ambulance,DriverProfile,IncidentCategory,AmbulanceTariff,AmbulanceDispatch,GPSPoint,NHIATariff,ETCClaim,ETCTreatmentItem]: admin.site.register(model,SimpleHistoryAdmin)
