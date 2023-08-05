"""Declares :class:`OAuth2ProviderRegistry`."""
from collections import defaultdict

from .....canon.idc import OAuth2ProviderSchema
from ..registry import BaseIdentityProviverRegistry
from .providers import GoogleOIDCProvider
from .providers import OIDCGenericProvider


class OAuth2ProviderRegistry(BaseIdentityProviverRegistry):
    """The registry for all OAuth2 providers."""
    provider_classes = defaultdict(lambda: OIDCGenericProvider, {
        'accounts.google.com': GoogleOIDCProvider
    })
    resource_kind = 'OAuth2Provider'
    schema_class = OAuth2ProviderSchema

    def __init__(self, oauth, *args, **kwargs):
        super().__init__()
        self.__oauth = oauth

    def get_provider_args(self, resource):
        """Returns the provider implementation class for the given
        resource.
        """
        return [self.__oauth], {}
