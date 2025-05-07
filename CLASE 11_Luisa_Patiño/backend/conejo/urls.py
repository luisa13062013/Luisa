
from rest_framework.routers import DefaultRouter
from .views import ConejoViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('conejos', ConejoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
