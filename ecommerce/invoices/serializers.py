from rest_framework import serializers
from .models import Invoice, InvoiceItem
from orders.serializers import OrderSerializer # Assuming you might want to nest or show order details
from catalog.serializers import ProductSerializer # Assuming you might want to nest or show product details

class InvoiceItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = InvoiceItem
        fields = ['id', 'invoice', 'product', 'product_details', 'quantity', 'unit_price', 'row_total']
        read_only_fields = ['row_total'] # Calculated in the model

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True) # Read-only nested items
    order_details = OrderSerializer(source='order', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'order', 'order_details', 'user', 'user_email',
            'issue_date', 'due_date', 'total_amount', 'payment_status', 'items'
        ]
        read_only_fields = ['invoice_number', 'issue_date', 'total_amount'] # Mostly set by the model or system

    # Optional: Add custom create logic if needed, e.g., to create invoice items
    # when an invoice is created, though often items are managed separately or
    # through a dedicated endpoint for adding items to an invoice if that's complex.
    # For now, we assume InvoiceItems might be created after Invoice creation,
    # or Invoice creation implies items are derived from the linked Order.

    def create(self, validated_data):
        # total_amount is set in the model's save method from the order
        invoice = Invoice.objects.create(**validated_data)
        return invoice
