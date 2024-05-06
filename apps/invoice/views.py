import pdfkit

# from django.shortcuts import render

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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


def generate_pdf_func(invoice, team):
    template_name = "pdf.html"

    if invoice.is_credit_for:
        template_name = "pdf_creditnote.html"

    template = get_template(template_name)
    html = template.render({"invoice": invoice, "team": team})
    pdf = pdfkit.from_string(html, False, options={})

    return pdf


# Generate PDFs for an invoice
@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def generate_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()

    pdf = generate_pdf_func(invoice, team)

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="invoice.pdf"'

    return response


@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def send_reminder(request, invoice_id):

    # send email with pdf of invoice
    invoice = get_object_or_404(Invoice, pk=invoice_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()

    if invoice:
        html_message = render_to_string("pdf.html", {"invoice": invoice})
        if invoice.is_credit_for:
            html_message = render_to_string("pdf_creditnote.html", {"invoice": invoice})
        # extracts plain text from html message without the tags.
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject="Payment reminder",
            body=plain_message,
            from_email=None,
            to=[invoice.client_email],
        )

        message.attach_alternative(html_message, "text/html")

        # attach pdf file to email---starts here

        pdf = generate_pdf_func(invoice, team)

        message.attach(
            filename=f"Invoice_{invoice.invoice_number}.pdf",
            content=pdf,
            mimetype="application/pdf",
        )
        # attach pdf file to email---ends here

        message.send()

        return Response({"message": "Successfully sent reminder"})
    return Response({"message": "Failed"})
