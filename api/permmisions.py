from rest_framework.permissions import BasePermission
import api.models as am
from rest_framework import permissions


class IsVerifiedUserPermission(BasePermission):
    """
    This permissions allow users access certain endpoint
    only when they are verified
    """

    def has_permission(self, request, view):

        if request.user.is_anonymous:
            return False
        else:
            return True
        
        
class IsOwnerOfApartmentPermission(BasePermission):
    
    def has_object_permissins(self, request, view, obj):
        if obj.owner == request.user:
            return True
        else:
            return False
