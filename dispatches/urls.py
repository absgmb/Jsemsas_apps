from rest_framework.routers import DefaultRouter
from .views import TariffViewSet,DispatchViewSet,GPSPointViewSet
router=DefaultRouter(); router.register("tariffs",TariffViewSet); router.register("dispatches",DispatchViewSet); router.register("gps",GPSPointViewSet)
urlpatterns=router.urls
