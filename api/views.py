from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
import api.serializers as aps
import api.models as am
from django.contrib.auth.hashers import check_password
import cloudinary
from django.db.models import Q, F
from rest_framework import viewsets
import api.permmisions as ap
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = aps.TokenObtainPairSerializer
    

class UserViewset(viewsets.ViewSet):
    
    @action(detail=False, methods=['post'])
    def upload_profile_image(self, request):
        '''
        profile image should be passed the the body
        of the request
        '''
        try:
            user = am.GidaUser.objects.get(username=request.user.username)
            serializer = aps.UserSerializer(data=request.data)
            if serializer.is_valid():
                data = request.data['image']
                # image = cloudinary.uploader.upload(data)
                # user.header_image = image['url']
                user.save()
            return Response({'header_image': data})
        except Exception:
            return Response({'status': 'Upload failed'})
        
    @action(detail=False, methods=['post'])
    def verify_password(self, request):
        try:
            email = request.user.email
            password = request.data['password']
            user = am.GidaUser.objects.get(email=email)  
            hash_password = user.password 
            password_checker = check_password(password, hash_password)
            if password_checker:
                return Response({'message': True})
            else:
                return Response({'message': False})
        except am.GidaUser.DoesNotExist:
            return Response({'message': 'Password or email do not match'})


class ApartmentViewset(viewsets.ModelViewSet):
    
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "get":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [ap.IsOwnerOfApartmentPermission]
        return [permission() for permission in self.permission_classes]
    queryset = am.Apartment.objects.all()
    serializer_class = aps.ApartmentSerializer
    
    def create(self, request, format=None):
        message = ''
        if 'image' not in request.data:
            # add default cloudinary images
            serializer = aps.ApartmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                message = "created"
        else:
            serializer = aps.ApartmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user, image=request.data['image'])
                message = "created"
        return Response(serializer.data or {'messsage': message})
    
    @action(detail=False)
    def search_apartment(self, request):
        try:
            apartment = am.Apartment.objects.filter(Q(location__icontains=self.request.query_params.get('location'))|
                                                    Q(state=self.request.query_params.get('state')),
                                                    room_type=self.request.query_params.get('room_type'),
                                                    is_active=True)
            serializer = aps.ApartmentSerializer(apartment, many=True)
        except am.Apartment.DoesNotExist:
            return Response({'message', 'Query does not match this criteria'})
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST'], permission_classes=[ap.IsVerifiedUserPermission])
    def book_apartment(self, request):
        try:
            message = ''
        
            apartment = am.Apartment.objects.get(id=self.request.query_params.get('apartment'), 
                                                    verified=True, is_active=True)
            available = am.BookedApartment.objects.filter(apartment=apartment, occupied=True).exists()
            if not available:
                user = am.GidaUser.objects.get(email=request.user.email)
                am.BookedApartment.objects.create(tenant=user, check_in=request.data['checkin'],
                                                check_out=request.data['checkout'],
                                                occupied=True, apartment=apartment)
                apartment.number_of_checkins = F('number_of_checkins') + 1
                apartment.save()
                message = 'Booked successfully'
            else:
                message = 'Apartment not available'
        except am.Apartment.DoesNotExist:
            message = 'Apartment may not be verified yet, do check back later'
                
        return Response({'message': message})
    
    @action(detail=False)
    def get_random_apartment(self, request):
        '''
        This methods returns 20 latest apartments
        to populate pages
        '''
        message = ''
        try:
            apartment = am.Apartment.objects.all().order_by('?')[:20]
            serializer = aps.ApartmentSerializer(apartment, many=True)
        except am.Apartment.DoesNotExist:
            message = 'Apartment does not exist'
        return Response(serializer.data or {'message': message})
    
    @action(detail=False)
    def get_apartment_by_id(self, request):
        # get apartment star
        response = {}
        try:
            apartment = am.Apartment.objects.get(id=self.request.query_params.get('id'), is_active=True)
            booked = am.BookedApartment.objects.filter(apartment=apartment)
            serializer = aps.ApartmentSerializer(apartment)
            serializer2 = aps.BookApartmentSerializer(booked, many=True)
            response = {
                "apartment": serializer.data,
                "bookings": serializer2.data
            }
        except am.Apartment.DoesNotExist:
            message = 'Apartment not found'
        except am.BookedApartment.DoesNotExist:
            message = 'Booked Apartment not found'
        return Response(response or {'message': message})
    
    @action(detail=False, permission_classes=[ap.IsOwnerOfApartmentPermission])
    def add_apartment_image(self, request):
        apartment = am.Apartment.objects.get(id=request.query_params.get('id'))
        image = apartment.images
        image.append(request.data['image'])
        apartment.save()
        return({'message': 'images saved'})
    
    @action(detail=False)
    def get_locations(self, request):
        location_tuple = am.LOCATION
        location_dict = dict((key, value) for key, value in location_tuple).keys()
        location_list = list(location_dict)
        return Response(location_list)
    
    @action(detail=False)
    def get_apartment_type(self, request):
        apartment_tuple = am.APARTMENT
        apartment_dict = dict((key, value) for key, value in apartment_tuple).keys()
        apartment_list = list(apartment_dict)
        return Response(apartment_list)
    
    @action(detail=False)
    def get_state(self, request):
        state_tuple = am.STATE
        state_dict = dict((key, value) for key, value in state_tuple).keys()
        state_list = list(state_dict)
        return Response(state_list)
    
    @action(detail=False)
    def get_country(self, request):
        country_tuple = am.COUNTRY
        country_dict = dict((key, value) for key, value in country_tuple).keys()
        country_list = list(country_dict)
        return Response(country_list)
    
    @action(detail=False)
    def toggle_checkin(self, request):
        message = ''
        try:
            apartment = am.Apartment.objects.get(id=self.request.query_params.get('apartment'),
                                                is_active=True)
            available = am.BookedApartment.objects.get(apartment=apartment, occupied=True).exists()
            if available:
                booked = am.BookedApartment.objects.get(apartment=apartment, occupied=True).exists()
                booked.occupied = False
                booked.save()
                message = 'checkout out'
            else:
                booked = am.BookedApartment.objects.get(apartment=apartment, occupied=True).exists()
                booked.occupied = True
                booked.save()
                message = 'checked in'
        except am.BookedApartment.DoesNotExist:
                message = 'You have not booked this apartment yet'
        return Response({'message': message})
    
    @action(detail=False)
    def toggle_apartment(self, request):
        # check if apartment is currently booked or less than the day booked
        # then deactivate it
        message = ''
        # get all bookings for that apartment
        # check if it is occupied
        try:
            apartment = am.Apartment.objects.get(id=self.request.query_params.get('apartment'),
                                                 is_active=True)
            bookings = am.BookedApartment.objects.filter(apartment=apartment)
            
            if not bookings.occupied:
                apartment.is_active = False
                apartment.save()
                message = 'Apartment deactivated'
            else:
                apartment.is_active = True
                apartment.save()
                message = 'Apartment activated'
        except am.Apartment.DoesNotExist:
            message = 'Apartment does not exist'
        return Response({'message': message})
    

# class ReviewViewSet(viewsets.ViewSet)
            
        
        
