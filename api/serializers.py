from rest_framework import serializers 
import api.models as am
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from  rest_registration.api.serializers import DefaultRegisterUserSerializer


class GidaUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = am.GidaUser
        exclude = ('password','user_permissions', 'groups', 
                   'is_staff', 'is_superuser', 'last_login')
        
    def create(self, validated_data):
        gidauser = am.GidaUser.objects.create_user(**validated_data)
        return gidauser


class ApartmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = am.Apartment
        fields = '__all__'


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['image'] = user.image
        token['id'] = user.id
        token['username'] = user.username

        return token
    
    
class DefaultRegisterUserSerializer(DefaultRegisterUserSerializer):
   # password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = am.GidaUser
        exclude = ('password','user_permissions', 'groups', 
                   'is_staff', 'is_superuser', 'last_login')


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
        return gidauser
