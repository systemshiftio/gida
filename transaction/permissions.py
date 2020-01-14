from rest_framework.permissions import BasePermission
from rest_framework import permissions
import transaction.models as tm


class CanUpdateTransaction(BasePermission):
    # nobody including admin can update transactions

    def has_permission(self, request, view):
        return False
    