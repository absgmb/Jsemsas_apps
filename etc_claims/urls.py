from rest_framework.routers import DefaultRouter
from .views import NHIATariffViewSet,ETCClaimViewSet,ETCTreatmentItemViewSet
router=DefaultRouter(); router.register("tariffs",NHIATariffViewSet); router.register("claims",ETCClaimViewSet); router.register("items",ETCTreatmentItemViewSet); urlpatterns=router.urls
