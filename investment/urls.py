from rest_framework import routers
from django.conf.urls import include
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter
import investment.views as iv

router = DefaultRouter(trailing_slash=False)
app_router = routers.DefaultRouter()
app_router.register('invest-apartment', iv.ApartmentViewset, 'invest-apartment')
app_router.register('personal-invest', iv.PersonalInvestmentViewset, 'personal-invest')





urlpatterns = [

    path('', include(app_router.urls)),
]