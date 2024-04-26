import pdfkit

# from django.shortcuts import render

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from rest_framework import viewsets, status, authentication, permissions
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

from .serializers import InvoiceSerializer, ItemSerializer
from .models import Invoice, Item
from apps.team.models import Team


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
            bankaccount=team.bankaccount,
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


# Generate PDFs for an invoice
@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def generate_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()
    template = get_template("pdf.html")
    html = template.render({"invoice": invoice, "team": team})
    pdf = pdfkit.from_string(html, False, options={})

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="invoice.pdf"'

    return response
