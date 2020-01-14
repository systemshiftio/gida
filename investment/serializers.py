from rest_framework import serializers
import api.models as am
import investment.models as im


class ApartmentInvestment(serializers.ModelSerializer):
    
    class Meta:
        model = im.Apartment
        fields = '__all__'
        

class InvestmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = im.PersonalInvestment
        fields = '__all__'