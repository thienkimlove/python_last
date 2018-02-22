from django.conf.urls import url
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView, CreateView, UpdateView

from core.models import Position
from core.tables import PositionJson
from core.views import *

app_name = "core"

class ContentIndexView(PermissionRequiredMixin, TemplateView):
    pass

class ContentCreateView(PermissionRequiredMixin, CreateView):
    pass

class ContentUpdateView(PermissionRequiredMixin, UpdateView):
    pass

class PositionIndex(ContentIndexView):
    template_name = "core/positions/index.html"
    permission_required = ('core.add_position', 'core.change_position', 'core.delete_position')


class BannerIndex(ContentIndexView):
    template_name = "core/banners/index.html"
    permission_required = ('core.add_banner', 'core.change_banner', 'core.delete_banner')

class PositionCreateView(ContentCreateView):
    model = Position
    template_name = "core/positions/create.html"
    permission_required = 'core.add_position'
    fields = ['name']

class PositionUpdateView(ContentUpdateView):
    model = Position
    template_name = "core/positions/edit.html"
    permission_required = 'core.change_position'
    fields = ['name']

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="core/index.html"), name='index'),
    url(r'^notice/$', TemplateView.as_view(template_name="core/notice.html"), name='notice'),
    url(r'^login/$', RedirectView.as_view(url=reverse_lazy('social:begin', args=['google-oauth2'])), name='login'),
    url(r'^logout/$', core_logout, name='logout'),
    url(r'^banners/$', BannerIndex.as_view(), name='banner_index'),
    url(r'^positions/dataTables/$', PositionJson.as_view(), name='position_data_tables'),
    url(r'^positions/create/$', PositionCreateView.as_view(), name='position_create'),
    url(r'^positions/(?P<pk>\d+)/edit', PositionUpdateView.as_view(), name='position_edit'),
    url(r'^positions/$', PositionIndex.as_view(), name='position_index'),
]