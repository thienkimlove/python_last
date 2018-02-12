from django.db.models import Q
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView

from core.models import Position


class PositionJson(BaseDatatableView):
    order_columns = ['id', 'name']

    def get_initial_queryset(self):
        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        # You should not filter data returned here by any filter values entered by user. This is because
        # we need some base queryset to count total number of records.
        return Position.objects

    def filter_queryset(self, qs):
        # use request parameters to filter queryset

        # simple example:
        search = self.request.GET.get(u'name', None)
        if search:
            qs = qs.filter(name__istartswith=search)

        # more advanced example
        filter_customer = self.request.GET.get(u'customer', None)

        if filter_customer:
            customer_parts = filter_customer.split(' ')
            qs_params = None
            for part in customer_parts:
                q = Q(customer_firstname__istartswith=part)|Q(customer_lastname__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            json_data.append({
                'id' : item.id,
                'name' : item.name,
                'created_at' : item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'action' : '<a class="table-action-btn" title="Chỉnh sửa vị trí" href="'+reverse('core_position_edit', kwargs={'pk': item.id})+'"><i class="fa fa-pencil text-success"></i></a>'
            })
        return json_data