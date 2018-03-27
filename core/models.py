from django.db import models

# Create your models here.
from django.urls import *

class GeneralCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 191
        super().__init__(*args, **kwargs)
        
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
    name = GeneralCharField(max_length=191)
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
    name = GeneralCharField(),
    slug = GeneralCharField()
    click_url = GeneralCharField()
    callback_url = GeneralCharField()
    map_params = GeneralCharField()
    extend_params = GeneralCharField()
    status = models.BooleanField()
    callback_allow_ip = GeneralCharField()
    is_sms_callback = models.SmallIntegerField()
    cron_url = GeneralCharField()
    auto = models.BooleanField()
    redirect_if_duplicate = GeneralCharField()
    number_redirect = models.SmallIntegerField()
    class Meta:
        db_table = 'networks'

class NetworkClick(TimeStampedModel):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    log_click_url = GeneralCharField()
    log_callback_url = GeneralCharField()
    sign = GeneralCharField()
    callback_ip = GeneralCharField()
    redirect_to_end_point_url = GeneralCharField()
    call_start_point_url = GeneralCharField()
    call_start_point_status = models.BooleanField(default=True)
    camp_ip = GeneralCharField()
    camp_time = GeneralCharField()
    callback_time = GeneralCharField()
    callback_response = GeneralCharField()
    origin = GeneralCharField()
    time = models.IntegerField()
    is_lead = models.BooleanField(default=False)
    class Meta:
        db_table = 'network_clicks'

class Report(TimeStampedModel):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    date = GeneralCharField()
    phone = GeneralCharField()
    class Meta:
        db_table = 'reports'
