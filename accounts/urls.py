from rest_framework.routers import DefaultRouter
from .views import UserViewSet,FacilityViewSet,AmbulanceViewSet,DriverProfileViewSet
router=DefaultRouter(); router.register("users",UserViewSet); router.register("facilities",FacilityViewSet); router.register("ambulances",AmbulanceViewSet); router.register("drivers",DriverProfileViewSet)
urlpatterns=router.urls
