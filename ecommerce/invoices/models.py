from django.db import models
from django.conf import settings # To get User model
from orders.models import Order
from catalog.models import Product
import uuid

class Invoice(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT) # Protect user from deletion if they have invoices
    invoice_number = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Invoice {self.invoice_number} for Order {self.order.id}"

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.order.total_price
        super().save(*args, **kwargs)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT) # Protect product from deletion if it's in an invoice
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    row_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Invoice {self.invoice.invoice_number}"

    def save(self, *args, **kwargs):
        if not self.row_total:
            self.row_total = self.quantity * self.unit_price
        super().save(*args, **kwargs)
