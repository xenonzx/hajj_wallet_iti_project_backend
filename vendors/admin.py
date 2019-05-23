from django.contrib import admin
from .models import Category , Vendor
from django.contrib import messages
from payments.models import Transaction
from custom_admin.admin import admin_site

class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 10

    list_display = ('name','description')

    actions = ['delete_model',]

    ## permissions
    def has_delete_permission(self, request, obj=None):
        return False

    ## actions
    def delete_model(self, request, queryset):
        for obj in queryset:
            temp=Vendor.objects.filter(category_id=obj.id)
            if len(temp) > 0:
                messages.error(request, "can't delete category with vendors")
            else:
                obj.delete()
                messages.success(request, "Category deleted successfully")
    delete_model.short_description = "Delete Category"

class VendorAdmin(admin.ModelAdmin):
    list_per_page = 10

    list_display = (
        'view_vendor_name',
        'view_vendor_email',
        'view_vendor_nationality',
            )

    list_filter = (
        'account__is_active',
        'account__nationality__name',
            )

    search_fields = ['account__nationality__name',
                     'account__username',
                     'account__first_name'
                     ]

    actions = [
        'block_vendors',
        'remove_blocked_vendors'
        ]

    fieldsets = (
        ("Personal info",
         {
             'fields':
                 (
                     'view_vendor_image',
                     'view_vendor_name',
                     'view_vendor_username',
                     'view_vendor_email',
                     'view_vendor_nationality',
                     'view_vendor_phone_number',
                 )
         }
         ),
        ("Shop Information",
         {
             'fields':
                 (
                    'crn',
                     'view_vendor_category',
                     'location',

                 )
         }
         ),
        ("Transactions",
         {
             'fields':
                 (
                    'show_vendor_transactions',
                 )
         }
         ),
    )

    ## permessions

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True

    ## changing methods names

    ## transactions
    def show_vendor_transactions(self,obj):
        vendor_transactions=Transaction.objects.select_related('pilgrim').filter(vendor_id=obj.account.id)
        if len(vendor_transactions) is 0:
            return None
        return "\n".join(["Received "+ str(t.money_paid)+" from "+str(t.pilgrim.username)  for t in vendor_transactions])

    show_vendor_transactions.short_description = 'Transactions'

    ## actions

    def block_vendors(self,request,queryset):
        for vendor in queryset:
            vendor.account.is_active = False
            vendor.account.save()
    block_vendors.short_description = 'Deactivate account'

    def remove_blocked_vendors(self, request, queryset):
        for vendor in queryset:
            vendor.account.is_active=True
            vendor.account.save()
    remove_blocked_vendors.short_description = 'Activate account'


admin_site.register(Category, CategoryAdmin)
admin_site.register(Vendor, VendorAdmin)
