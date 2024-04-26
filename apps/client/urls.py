from django.urls import path, include

from rest_framework import routers

from .views import ClientViewSet, update_client

router = routers.DefaultRouter()
router.register(r"clients", ClientViewSet, basename="clients")

urlpatterns = [
    path("update_client/<int:id>/", update_client, name="update_client"),
    path("", include(router.urls)),
]
