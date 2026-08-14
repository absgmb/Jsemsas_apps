from rest_framework import viewsets
from .models import IncidentCategory
from .serializers import IncidentCategorySerializer
from accounts.permissions import Dispatchers
class IncidentCategoryViewSet(viewsets.ModelViewSet):
 queryset=IncidentCategory.objects.filter(is_active=True); serializer_class=IncidentCategorySerializer; permission_classes=[Dispatchers]
