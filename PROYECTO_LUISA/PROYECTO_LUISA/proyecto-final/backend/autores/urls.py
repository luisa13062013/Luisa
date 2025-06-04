from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AutorViewSet

router = DefaultRouter()
router.register(r'', AutorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
