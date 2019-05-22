from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from accounts.models import Account
from pilgrims.models import Pilgrims
from vendors.models import Vendor, Category
from django.db.models import Count




class MyAdminSite(AdminSite):

    def index(self, request, extra_context=None):

        users = Account.objects.filter(is_staff=1).count()
        pilgrims = Pilgrims.objects.all().count()
        vendors = Vendor.objects.all().count()
        categories = Category.objects.all().count()


        # statis = Vendor.objects.prefetch_related('category').values(
        #     'category__name') \
        #     .annotate(dcount=Count('category__name'))
        #
        # print(statis.values_list('dcount', flat=True))
        # print(statis.values_list('category__name', flat=True))

        app_list = self.get_app_list(request)

        context = {
            **self.each_context(request),
            'title': self.index_title,
            'app_list': app_list,
            **(extra_context or {}),
            'users': users,
            'pilgrims':pilgrims,
            'vendors':vendors,
            'categories':categories
        }

        request.current_app = self.name

        return TemplateResponse(request, self.index_template or 'admin/index.html', context)

admin_site = MyAdminSite()