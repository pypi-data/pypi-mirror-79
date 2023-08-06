"""Declares :class:`GoogleOIDCProvider`."""
from .oidc import OIDCGenericProvider


class GoogleOIDCProvider(OIDCGenericProvider):
    """Implements OAuth2 with Google using OpenID Connect (OIDC)."""
    metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

    @staticmethod
    def get_client_kwargs(spec): # pylint: disable=arguments-differ
        """Return the client keyword arguments for the specified
        provider `spec`.
        """
        kwargs = {}
        if spec.get('scope'):
            kwargs['scope'] = str.join(' ', spec['scope'])
        return kwargs

    def get_asserted_subject_id(self, cs):
        """Return the asserted subject identifier from the OAuth2 provider
        claims set.
        """
        return f"{cs['sub']}@accounts.google.com"
