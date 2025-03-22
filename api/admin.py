from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('name', 'email', 'amount', 'reference', 'status', 'created_at')
    
    # Fields to filter by in the sidebar
    list_filter = ('status', 'created_at')
    
    # Fields to search
    search_fields = ('name', 'email', 'reference')
    
    # Fields to make read-only
    readonly_fields = ('reference', 'created_at')
    
    # Ordering of records
    ordering = ('-created_at',)
    
    # Customize the list view with pagination
    list_per_page = 25

    # Optionally, customize fieldsets for the detail view
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'amount', 'reference', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)  # Collapsible section
        }),
    )

    # Add actions (e.g., mark as completed)
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        queryset.update(status='success')
        self.message_user(request, "Selected payments marked as completed.")
    mark_as_completed.short_description = "Mark selected payments as completed"