from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
import api.serializers as aps
import api.models as am
import transaction.models as tm
from django.db.models import Q, F
from rest_framework import viewsets
from rest_framework import permissions
import transaction.permissions as tp
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.


class TransactionViewset(viewsets.ViewSet):
    '''
    pass the book id as a query parameter like this
    get_list_of_chapters/?id=<value>
    '''
    def get_permissions(self):
        if self.action == "update" or "delete":
            self.permission_classes = [tp.CanUpdateTransaction]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]
    
    @action(detail=False, methods=['post'])
    def create_transaction(self, request):
        try:
            pass
        except:
            return Response({'message': 'Password or email do not match'})