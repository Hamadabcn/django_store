from django.contrib import admin
from reports.models import OrderReport
from store.models import Order
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek
from django.db.models import Sum
import json


@admin.register(OrderReport)
class OrderAdmin(admin.ModelAdmin):

    change_list_template = 'admin/reports/orders.html'

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):

        yearly_stats = (
            Order.objects.select_related('transaction')
            .annotate(year=ExtractYear('created_at'))
            .values('year')
            .annotate(sum=Sum('transaction__amount'))
        )

        monthly_stats = (
            Order.objects.select_related('transaction')
            .annotate(year=ExtractYear('created_at'))
            .annotate(month=ExtractMonth('created_at'))
            .values('year', 'month')
            .annotate(sum=Sum('transaction__amount'))[:30]
        )

        weekly_stats = (
            Order.objects.select_related('transaction')
            .annotate(year=ExtractYear('created_at'))
            .annotate(week=ExtractWeek('created_at'))
            .values('year', 'week')
            .annotate(sum=Sum('transaction__amount'))[:30]
        )

        context = {
            **self.admin_site.each_context(request),
            'yearly_stats': json.dumps(list(yearly_stats)),
            'monthly_stats': json.dumps(list(monthly_stats)),
            'weekly_stats': json.dumps(list(weekly_stats)),
            'title': _('Orders Report')
        }

        return TemplateResponse(
            request, self.change_list_template, context
        )
