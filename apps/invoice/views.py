from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import InvoiceSerializer, ItemSerializer
from .models import Invoice, Item
from apps.team.models import Team

from django.core.exceptions import PermissionDenied


# Create your views here.
class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        team = self.request.user.teams.first()

        # automated assignment of invoice number
        invoice_number = team.first_invoice_number + 1
        team.first_invoice_number = invoice_number
        team.save()

        return serializer.save(
            created_by=self.request.user,
            modified_by=self.request.user,
            team=team,
            invoice_number=invoice_number,
        )

    def perform_update(self, serializer):
        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied("You do not have access")

        serializer.save(modified_by=self.request.user)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get_queryset(self):
        invoice_id = self.request.GET.get("invoice_id", 0)
        return self.queryset.filter(invoice__id=invoice_id)
