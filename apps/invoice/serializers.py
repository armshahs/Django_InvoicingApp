from rest_framework import serializers

from .models import Invoice, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        read_only_fields = (
            "invoice",
            "net_amount",
        )
        fields = (
            "id",
            "title",
            "quantity",
            "unit_price",
            "net_amount",
            "vat_rate",
            "discount",
        )


class InvoiceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Invoice
        read_only_fields = (
            "team",
            "invoice_number",
            "created_at",
            "modified_at",
            "modified_by",
            "created_by",
        )
        fields = (
            "id",
            "invoice_number",
            "client",
            "client_name",
            "client_email",
            "client_org_number",
            "client_address_1",
            "client_address_2",
            "client_zipcode",
            "client_place",
            "client_country",
            "client_contact_person",
            "client_contact_reference",
            "sender_reference",
            "invoice_type",
            "due_days",
            "is_sent",
            "is_paid",
            "gross_amount",
            "vat_amount",
            "net_amount",
            "discount_amount",
            "items",
        )

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        invoice = Invoice.objects.create(**validated_data)

        for item in items_data:
            Item.objects.create(invoice=invoice, **item)

        return invoice
