from django.conf.urls import url

from core.tables import PositionJson
from core.views import *

urlpatterns = [
    url(r'^$', index, name='core_index'),
    url(r'^banners', banners, name='core_banner_index'),
    url(r'^positions/dataTables/$', PositionJson.as_view(), name='core_position_data_tables'),
    url(r'^positions', positions, name='core_position_index'),
]