from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_length(value):
    if len(value) < 4:
        raise ValidationError(
            _('%(value)s must greater than 3'),
            params={'value': value},
        )

class PositionForm(forms.Form):
    name = forms.CharField(max_length=30, label='Tên', validators=[validate_length])