from rest_framework import serializers 
import api.models as am
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from  rest_registration.api.serializers import DefaultRegisterUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class GidaUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = am.GidaUser
        exclude = ('password','user_permissions', 'groups', 
                   'is_staff', 'is_superuser', 'last_login')
        
    def create(self, validated_data):
        gidauser = am.GidaUser.objects.create_user(**validated_data)
        return gidauser
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = am.GidaUser
        fields = '__all_'



class ApartmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = am.Apartment
        fields = '__all__'
        
    
class BookApartmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = am.BookedApartment
        fields = ('check_in', 'check_out')


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['image'] = user.image
        token['id'] = user.id
        token['username'] = user.username

        return token 
    
class RegisterToken(serializers.Serializer):
    access_token = serializers.CharField(max_length=1000)
    refresh = serializers.CharField(max_length=1000)
    
    class Meta:
        fields = ('access_token', 'refesh')
    
    
class DefaultRegisterUserSerializer(DefaultRegisterUserSerializer):
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        refresh['image'] = user.image
        refresh['id'] = user.id
        refresh['username'] = user.username
        refresh['phone'] = user.phone
        refresh['email'] = user.email
        return{
            'access_token': str(refresh.access_token),
            'refresh': str(refresh.access_token),
            }
   
    class Meta:
        model = am.GidaUser

    def create(self, validated_data):
        email_message = """
                You have Signed up for Gida
                """
        # use signals to send mail after user has been saved
        if 'image' in validated_data:
            image_url = validated_data['image']
            # image = cloudinary.uploader.upload(image_url)
            gidauser = am.GidaUser.objects.create_user(**validated_data)
            gidauser.image = image['url']
            gidauser.save()
            # send_mail(
            #         'Signed Up',
            #         email_message,
            #         'welcome@gida.africa',
            #         [validated_data['email']],
            #         fail_silently=False
            #         )
        else:
            gidauser = am.GidaUser.objects.create_user(**validated_data)
            # send_mail(
            #         'Signed Up',
            #         email_message,
            #         'welcome@gida.africa',
            #         [validated_data['email']],
            #         fail_silently=False
            #         )
            response =self.get_tokens_for_user(gidauser)
        return response
