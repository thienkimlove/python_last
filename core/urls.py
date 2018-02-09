from django.conf.urls import url

from core.views import *

urlpatterns = [
    url(r'^$', index, name='core_index'),
    url(r'^banners', banners, name='core_banner_index'),
]