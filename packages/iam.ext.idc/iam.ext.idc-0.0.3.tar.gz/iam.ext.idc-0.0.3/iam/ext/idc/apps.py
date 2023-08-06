"""Declares :class:`IdentityConsumerConfig`."""
import ioc
from django.apps import AppConfig
from django.apps import apps

from .infra import SubjectRepository


class IdentityConsumerConfig(AppConfig):
    """Configures the :mod:`iam.ext.idc` package."""
    name = 'iam.ext.idc'
    label = 'idc'
    verbose_name = "IAM - Identity Consumer"

    def ready(self):
        """Invoked when the Django app registry has loaded all
        apps.
        """
        ioc.provide('iam.SubjectRepository', SubjectRepository())
        ioc.provide('iam.SubjectFactory', apps.get_model('idc.AssertedSubject'))
