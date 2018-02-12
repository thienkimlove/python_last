from django.conf.urls import url

from core.tables import PositionJson
from core.views import *

urlpatterns = [
    url(r'^$', index, name='core_index'),
    url(r'^banners', banner_list, name='core_banner_index'),
    url(r'^positions/dataTables/$', PositionJson.as_view(), name='core_position_data_tables'),
    url(r'^positions/create', position_create, name='core_position_create'),
    url(r'^positions/(?P<pk>\d+)/edit', position_edit, name='core_position_edit'),
    url(r'^positions', position_list, name='core_position_index'),
]