from django.urls import path, include

from rest_framework import routers

from .views import InvoiceViewSet, ItemViewSet, generate_pdf, send_reminder


router = routers.DefaultRouter()
router.register(r"invoices", InvoiceViewSet, basename="invoices")
router.register(r"items", ItemViewSet, basename="items")

urlpatterns = [
    path("", include(router.urls)),
    path("invoices/<int:invoice_id>/generate_pdf/", generate_pdf, name="generate_pdf"),
    path(
        "invoices/<int:invoice_id>/send_reminder/", send_reminder, name="send_reminder"
    ),
]
