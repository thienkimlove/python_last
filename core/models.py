from django.db import models

# Create your models here.
from django.urls import reverse


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
