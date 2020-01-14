from django.shortcuts import render
from rest_framework import viewsets
import investment.permissions as ip
import investment.serializers as ins
import investment.models as im
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.


class ApartmentViewset(viewsets.ModelViewSet):
    
    permission_classes = [IsAdminUser,]
    queryset = im.Apartment.objects.all()
    serializer_class = ins.ApartmentInvestment
    
    def create(self, request, format=None):
        message = ''
        serializer = ins.ApartmentInvestment(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = 'created'
        else:
            message = 'Something went wrong, check input'
        return Response(serializer.data or {'messsage': message})
    
    
class PersonalInvestmentViewset(viewsets.ViewSet):
    
    @action(detail=False)
    def get_all_active_investment(self, request):
        try:
            investment = im.PersonalInvestment.objects.filter(owner=request.user, active=True)
            serializer = ins.InvestmentSerializer(investment, many=True)
            response = {
                'data': serializer.data
            }
        except im.PersonalInvestment.DoesNotExist:
            response = {
                'message' :'You have no active investment'
            }
        return Response(response)
    
    @action(detail=False)
    def get_all_investment(self, request):
        message = ''
        try:
            investment = im.PersonalInvestment.objects.filter(owner=request.user)
            serializer = ins.InvestmentSerializer(investment, many=True)
            response = {
                'data': serializer.data
            }
        except im.PersonalInvestment.DoesNotExist:
            response = {
                'message' :'You have no active investment'
            }
        return Response(response)
    
        