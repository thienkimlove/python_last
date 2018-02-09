from django.conf.urls import url

from frontend.views import index

urlpatterns = [
    url(r'^$', index, name='frontend_index'),
]