from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderReport(models.Model):
    class Meta:
        verbose_name_plural = _('Orders')
