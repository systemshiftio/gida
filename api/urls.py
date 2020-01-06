from rest_framework import routers
from django.conf.urls import include
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter
import api.views as av

router = DefaultRouter(trailing_slash=False)
app_router = routers.DefaultRouter()
app_router.register('search-apartment', av.SearchApartmentViewset, 'search-apartment')




urlpatterns = [

    # documentation
    path('', include(app_router.urls)),
    # path('oauth/login/', av.SocialLoginView.as_view())

]