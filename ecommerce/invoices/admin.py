from django.contrib import admin
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0 # Number of empty forms to display
    readonly_fields = ('product', 'quantity', 'unit_price', 'row_total') # Make items read-only when viewed through Invoice
    can_delete = False # Optionally prevent deleting items from here

    def has_add_permission(self, request, obj=None):
        return False # Prevent adding new items directly from the Invoice admin

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'order_id_display', 'user_email_display', 'issue_date', 'due_date', 'total_amount', 'payment_status')
    list_filter = ('payment_status', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'order__id', 'user__email')
    readonly_fields = ('invoice_number', 'order', 'user', 'total_amount', 'issue_date') # Fields not editable in admin
    inlines = [InvoiceItemInline]

    def order_id_display(self, obj):
        return obj.order.id
    order_id_display.short_description = 'Order ID'

    def user_email_display(self, obj):
        return obj.user.email
    user_email_display.short_description = 'User Email'

    def has_add_permission(self, request):
        # Typically, invoices are generated from orders, not manually created
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of invoices from admin, or add specific conditions
        return False

admin.site.register(Invoice, InvoiceAdmin)

# It's usually not necessary to register InvoiceItem separately
# if it's primarily managed via Invoice, but if direct access is needed:
# class InvoiceItemAdmin(admin.ModelAdmin):
#     list_display = ('invoice', 'product', 'quantity', 'unit_price', 'row_total')
#     search_fields = ('invoice__invoice_number', 'product__name')
#     readonly_fields = ('invoice', 'product', 'quantity', 'unit_price', 'row_total')

#     def has_add_permission(self, request):
#         return False
#     def has_change_permission(self, request, obj=None):
#         return False
#     def has_delete_permission(self, request, obj=None):
#         return False

# admin.site.register(InvoiceItem, InvoiceItemAdmin)
