from django.contrib import admin
from custom_admin.admin import admin_site
from pilgrims.models import Pilgrims
from payments.models import Transaction

class PilgrimAdmin(admin.ModelAdmin):

    list_per_page = 10


    list_display = (
        'show_pilgrim_name',
        'show_pilgrim_username',
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

    def show_pilgrim_name(self, obj):
        return obj.account.first_name + " " + obj.account.last_name

    show_pilgrim_name.short_description = 'Name'

    def show_pilgrim_email(self,obj):
        return obj.account.email
    show_pilgrim_email.short_description = 'Email'

    def show_pilgrim_nationality(self,obj):
        return obj.account.nationality
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
        pilgrim_transactions=Transaction.objects.select_related('vendor').filter(pilgrim_id=obj.account.id)
        if len(pilgrim_transactions) is 0:
            return None
        return "\n".join(["Received " + str(t.money_paid) + " from " + str(t.pilgrim.username) for t in pilgrim_transactions])

    show_pilgrim_transactions.short_description = 'transaction'

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     p=Pilgrims.objects.get(id=int(object_id))
    #     print(p.pilgrim_account_id.all()) ### reverse relation
    #     print(object_id)
    #     return None



admin_site.register(Pilgrims, PilgrimAdmin)

