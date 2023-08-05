"""Declares :class:`OIDCGenericProvider`."""
from .base import BaseOAuth2Provider


class OIDCGenericProvider(BaseOAuth2Provider):
    """Generic implementation of OAuth2 using the OpenID Connect (OIDC)
    protocol.
    """
    metadata_url = None

    @classmethod
    def fromresource(cls, resource, oauth, *args, **kwargs): # pylint: disable=arguments-differ
        """Create a new :class:`OIDCGenericProvider` from a provider
        resource.
        """
        meta = resource['metadata']
        spec = dict(resource['spec'])
        credentials = spec.pop('credentials')
        if not cls.metadata_url:
            raise NotImplementedError
        return cls.fromclient(
            oauth.register(
                name=meta['name'],
                server_metadata_url=cls.metadata_url,
                client_id=credentials['id'],
                client_secret=credentials['secret'],
                client_kwargs=cls.get_client_kwargs(spec)
            ), *args, **spec
        )

    @staticmethod
    def get_client_kwargs(*args, **kwargs): # pylint: disable=unused-argument
        """Return the client keyword arguments for the specified
        provider `spec`.
        """
        return None

    def get_asserted_subject_id(self, cs): # pylint: disable=invalid-name
        """Return the asserted subject identifier from the OAuth2 provider
        claims set.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def is_default(self):
        """Return a boolean indicating if the provider is the default
        provider for a protocol.
        """
        return self.__is_default

    def is_enabled(self):
        """Return a boolean indicating if the provider is enabled
        for a protocol.
        """
        return True
