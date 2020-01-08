from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
import api.serializers as aps
import api.models as am
from django.db.models import Q, F
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = aps.TokenObtainPairSerializer


class SearchApartmentViewset(viewsets.ViewSet):
    
    @action(detail=False)
    def search_apartment(self, request):
        try:
            apartment = am.Apartment.objects.filter(Q(address=self.request.query_params.get('address')) |
                                                   Q(price=self.request.query_params.get('price')),                                           
                                                    location=self.request.query_params.get('location'),
                                                    state=self.request.query_params.get('state'))
            serializer = aps.ApartmentSerializer(apartment, many=True)
        except am.Apartment.DoesNotExist:
            return Response({'message', 'Apartment does not exist'})
        return Response(serializer.data)
    
    
class BookApartment(viewsets.ViewSet):
    
    @action(detail=False, methods=['POST'])
    def book_apartment(self, request):
        message = ''
        availability = am.Apartment.objects.get(apartment=self.request.query_params.get('apartment'), 
                                                occupied=False,
                                                verified=True)
        if availability:
            availability.occupied = True
            availability.number_of_checkins = F('number_of_checkins') + 1
            message = 'Booked successfully'
        else:
            message = 'Something went wrong'
        return Response({'message': message})
    


