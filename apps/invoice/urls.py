from django.urls import path, include

from rest_framework import routers

from .views import InvoiceViewSet, ItemViewSet


router = routers.DefaultRouter()
router.register(r"invoices", InvoiceViewSet, basename="invoices")
router.register(r"items", ItemViewSet, basename="items")

urlpatterns = [
    path("", include(router.urls)),
]
