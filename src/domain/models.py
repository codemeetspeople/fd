from django.db import models
from django.utils.translation import gettext as _


class Message(models.Model):
    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['-created_at']

    origin_message = models.TextField(verbose_name=_('Origin message'), null=False)
    message_element = models.CharField(max_length=255, verbose_name=_('Message element'), null=False)
    resolution = models.CharField(max_length=50, verbose_name=_('Resolution'), null=False)
    found = models.BooleanField(default=False, verbose_name=_('Found'), null=False)
    probable = models.BooleanField(default=False, verbose_name=_('Probable'), null=False)

    ip = models.GenericIPAddressField(verbose_name=_('IP address'), null=False)

    created_at = models.DateTimeField(auto_now_add=True)
