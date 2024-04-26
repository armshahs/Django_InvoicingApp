from django.contrib.auth.models import User
from django.db import models

from apps.client.models import Client
from apps.team.models import Team


# Create your models here.
class Invoice(models.Model):
    INVOICE = "invoice"
    CREDIT_NOTE = "credit_note"

    CHOICES_TYPE = (
        (INVOICE, "Invoice"),
        (CREDIT_NOTE, "Credit_note"),
    )

    invoice_number = models.IntegerField(default=1)

    client_name = models.CharField(max_length=255)
    client_email = models.CharField(max_length=255)
    client_org_number = models.CharField(max_length=255, blank=True, null=True)
    client_address_1 = models.CharField(max_length=255, blank=True, null=True)
    client_address_2 = models.CharField(max_length=255, blank=True, null=True)
    client_zipcode = models.CharField(max_length=255, blank=True, null=True)
    client_place = models.CharField(max_length=255, blank=True, null=True)
    client_country = models.CharField(max_length=255, blank=True, null=True)
    client_contact_person = models.CharField(max_length=255, blank=True, null=True)
    client_contact_reference = models.CharField(max_length=255, blank=True, null=True)

    sender_reference = models.CharField(max_length=255, blank=True, null=True)
    invoice_type = models.CharField(
        max_length=20, choices=CHOICES_TYPE, default=INVOICE
    )
    due_days = models.IntegerField(default=14)
    # Only for credit notes:
    is_credit_for = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    is_sent = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    gross_amount = models.DecimalField(max_digits=6, decimal_places=2)
    vat_amount = models.DecimalField(max_digits=6, decimal_places=2)
    net_amount = models.DecimalField(max_digits=6, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=6, decimal_places=2)

    team = models.ForeignKey(Team, related_name="invoices", on_delete=models.CASCADE)
    client = models.ForeignKey(
        Client, related_name="invoices", on_delete=models.CASCADE
    )

    modified_by = models.ForeignKey(
        User, related_name="modified_invoices", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name="created_invoices", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.invoice_number} - {self.client_name} - {self.invoice_type}"


class Item(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    net_amount = models.DecimalField(max_digits=6, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Calculate the net amount as the product of quantity and unit_price
        self.net_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)
