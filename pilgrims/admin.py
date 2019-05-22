from django.contrib import admin
from pilgrims.models import Pilgrims
from payments.models import Transaction

@admin.register(Pilgrims)
class PilgrimAdmin(admin.ModelAdmin):

    list_per_page = 10
    list_display = (
        'show_pilgrim_name',
        'show_pilgrim_email',
        'show_pilgrim_nationality',
        )

    list_filter = (
        'account__is_active',
        'account__nationality__name'
        )

    search_fields = ['account__nationality__name',
                     'account__username',
                     'account__first_name']
    fieldsets = (
                    ("Personal info",
                     {
                        'fields':
                            (
                            'show_pilgrim_image',
                            'show_pilgrim_name',
                            'show_pilgrim_username',
                            'show_pilgrim_email',
                            'show_pilgrim_nationality',
                            'show_pilgrim_phone_number',
                            )
                     }
                    ),
                    ("Transactions",
                     {
                         'fields':
                             (
                                'show_pilgrim_transactions',
                             )
                     }
                     ),
                )

    ### permessions allowed
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True

    ### customize list display

    def show_pilgrim_name(self,obj):
        return obj.account.first_name+" "+obj.account.last_name
    show_pilgrim_name.short_description = 'Name'

    def show_pilgrim_email(self,obj):
        return obj.account.email
    show_pilgrim_email.short_description = 'Email'

    def show_pilgrim_nationality(self,obj):
        return obj.account.nationality.name
    show_pilgrim_nationality.short_description = 'Nationality'

    def edit_pilgrim_is_active(self,obj):
        return obj.account.is_active
    edit_pilgrim_is_active.short_description = 'Status'

    def show_pilgrim_image(self,obj):
        return obj.account.image
    show_pilgrim_image.short_description = 'image'

    def show_pilgrim_phone_number(self,obj):
        return obj.account.phone_number
    show_pilgrim_phone_number.short_description = 'Phone number'

    def show_pilgrim_username(self,obj):
        return obj.account.username
    show_pilgrim_username.short_description = 'Username'

    def show_pilgrim_transactions(self,obj):
        temp=Transaction.objects.filter(pilgrim_id=obj.account)
        if len(temp) is 0:
            return None
        return
    show_pilgrim_transactions.short_description = 'transaction'



