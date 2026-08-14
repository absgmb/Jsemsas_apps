from rest_framework.routers import DefaultRouter
from .views import IncidentCategoryViewSet
router=DefaultRouter(); router.register("categories",IncidentCategoryViewSet); urlpatterns=router.urls
