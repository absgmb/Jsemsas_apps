from rest_framework.permissions import BasePermission
class RolePermission(BasePermission):
 allowed_roles=set()
 def has_permission(self,request,view): return bool(request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.role in self.allowed_roles))
class AdminOnly(RolePermission): allowed_roles={"SUPER_ADMIN"}
class FacilityAdmins(RolePermission): allowed_roles={"SUPER_ADMIN","FACILITY_ADMIN"}
class Dispatchers(RolePermission): allowed_roles={"SUPER_ADMIN","FACILITY_ADMIN","DISPATCHER"}
class Drivers(RolePermission): allowed_roles={"SUPER_ADMIN","DRIVER"}
class Nurses(RolePermission): allowed_roles={"SUPER_ADMIN","NURSE","FACILITY_ADMIN"}
