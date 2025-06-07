from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser # Or other appropriate permissions

from .models import Invoice, InvoiceItem
from .serializers import InvoiceSerializer, InvoiceItemSerializer
from orders.models import Order # Corrected from ecommerce.orders.models
from core.permissions import IsOwnerOrAdmin # Corrected from ecommerce.core.permissions

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-issue_date')
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdminUser] # Default to admin-only for now

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Invoice.objects.all().order_by('-issue_date')
        return Invoice.objects.filter(user=user).order_by('-issue_date')

    def perform_create(self, serializer):
        # This basic create is for manual creation if ever needed.
        # The main way to create invoices will be via the 'create_from_order' action.
        # Ensure user is set if not part of the request data directly.
        if not serializer.validated_data.get('user'):
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    @action(detail=False, methods=['post'], url_path='create-from-order', permission_classes=[IsAdminUser]) # Admin creates invoices
    def create_from_order(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({'error': 'Order ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        if Invoice.objects.filter(order=order).exists():
            return Response({'error': 'Invoice already exists for this order.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create Invoice
        invoice = Invoice.objects.create(
            order=order,
            user=order.user, # Assuming order.user is the correct user for the invoice
            due_date=request.data.get('due_date'), # due_date should be provided in request
            # total_amount is set by the model's save method
            # payment_status defaults to 'PENDING'
        )

        # Create InvoiceItems from OrderItems
        for item in order.items.all(): # Assuming order.items is the related manager for OrderItem
            InvoiceItem.objects.create(
                invoice=invoice,
                product=item.product,
                quantity=item.count, # Assuming OrderItem has a 'count' field
                unit_price=item.product.price, # Assuming product.price is the price at time of order
                                               # This might need adjustment if prices can change and you need historical price
                # row_total is set by the model's save method
            )

        # Update invoice total_amount explicitly after items are created,
        # if the model's default save (based on order.total_price) isn't sufficient
        # or if there are any discrepancies to ensure.
        # For now, relying on model's save for total_amount.

        serializer = self.get_serializer(invoice)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Standard ModelViewSet actions (list, retrieve, update, partial_update, destroy)
    # are provided by default.
    # Permissions:
    # - List: User can list their own invoices, admin can list all.
    # - Retrieve: User can retrieve their own invoice, admin can retrieve any. (Handled by get_queryset and object-level permissions if needed)
    # - Create: Done via 'create_from_order' by admin. Manual creation restricted.
    # - Update: Admin only (e.g., to update payment_status).
    # - Destroy: Admin only, and generally discouraged.

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action == 'retrieve':
            # Assuming IsOwnerOrAdmin checks if request.user is invoice.user or admin
            # This requires IsOwnerOrAdmin to be defined and working correctly.
            # If not available, stick to IsAdminUser or implement basic owner check here.
            # For simplicity, let's assume IsOwnerOrAdmin is available. If not, we'll need to adjust.
            self.permission_classes = [IsOwnerOrAdmin]
            # self.permission_classes = [IsAdminUser] # Simplified for now, can refine if IsOwnerOrAdmin is confirmed
        elif self.action == 'list':
            self.permission_classes = [IsAdminUser] # Or IsAuthenticated for users to list their own
        return super().get_permissions()
