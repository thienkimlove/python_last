from django.db import models

# Create your models here.
from django.urls import *


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides selfupdating
    ``created`` and ``modified`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Position(TimeStampedModel):
    name = models.CharField(max_length=191)
    class Meta:
        db_table = 'positions'

    def get_absolute_url(self):
        return reverse('core:position_index')


class Banner(TimeStampedModel):
    #class CharField(max_length=None, **options)
    link = models.URLField(max_length=191)
    #class ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)
    # path for image in template is {{ object.image.url }}.
    image = models.ImageField(upload_to='', max_length=191)
    #class ForeignKey(to, on_delete, **options)
    #A many-to-one relationship. Requires two positional arguments: the class to which the model is related and the on_delete option
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    class Meta:
        db_table = 'banners'

    def get_absolute_url(self):
        return reverse('core:banner_index')

class Network(TimeStampedModel):
    name = models.CharField(),
    slug = models.CharField()
    click_url = models.CharField()
    callback_url = models.CharField()
    map_params = models.CharField()
    extend_params = models.CharField()
    status = models.BooleanField()
    callback_allow_ip = models.CharField()
    is_sms_callback = models.SmallIntegerField()
    cron_url = models.CharField()
    auto = models.BooleanField()
    redirect_if_duplicate = models.CharField()
    number_redirect = models.SmallIntegerField()
    class Meta:
        db_table = 'networks'

class NetworkClick(TimeStampedModel):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    log_click_url = models.CharField()
    log_callback_url = models.CharField()
    sign = models.CharField()
    callback_ip = models.CharField()
    redirect_to_end_point_url = models.CharField()
    call_start_point_url = models.CharField()
    call_start_point_status = models.BooleanField(default=True)
    camp_ip = models.CharField()
    camp_time = models.CharField()
    callback_time = models.CharField()
    callback_response = models.CharField()
    origin = models.CharField()
    time = models.IntegerField()
    is_lead = models.BooleanField(default=False)
    class Meta:
        db_table = 'network_clicks'

class Report(TimeStampedModel):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    date = models.CharField()
    phone = models.CharField()
    class Meta:
        db_table = 'reports'
