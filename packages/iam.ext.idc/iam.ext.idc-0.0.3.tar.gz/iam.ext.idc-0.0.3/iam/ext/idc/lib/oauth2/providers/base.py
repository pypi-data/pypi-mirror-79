# pylint: disable=invalid-name
"""Declares :class:`BaseOAuth2Provider`."""
import ioc

from ...provider import BaseProvider


class BaseOAuth2Provider(BaseProvider):
    """The base class for all OAuth2 providers."""

    @property
    def name(self):
        """Return the name with which the client was registered in the
        :mod:`authlib` library.
        """
        return self.__client.name

    @property
    def description(self):
        """Return the description as specified in the resource."""
        return self.__description

    def __init__(self, client, description, external, superusers, **kwargs):
        self.__client = client
        self.__description = description
        self.__external = external
        self.__superusers = superusers
        self.__is_default = kwargs.get('is_default')

    @classmethod
    def fromclient(cls, client, *args, **kwargs):
        """Return a new :class:`BaseOAuth2Provider` from a :mod:`authlib`
        OAuth2 client object.
        """
        return cls(client, *args, **kwargs)

    def authorize_redirect(self, request, redirect_to):
        """Initiate the OAuth2 login dialog by redirecting the user to the
        SSO provider login screen.
        """
        return self.__client.authorize_redirect(request, redirect_to)

    def get_asserted_subject(self, request):
        """Invoked after the OAuth2 provider redirects the client upon
        succesfully completing the authentication dialog.
        """
        return self.authenticate(
            request,
            token=self.__client.authorize_access_token(request),
            provider=self
        )

    def is_default(self):
        """Indicates if the provider is the default provider."""
        return self.__is_default

    @ioc.inject('subjects', 'iam.SubjectRepository')
    @ioc.inject('factory', 'iam.SubjectFactory')
    def token_to_subject(self, request, token, subjects, factory):
        """Exchange an access token for an OIDC ID token, and get or
        create a corresponding :term:`Subject` from the persistent
        data store.
        """
        cs = self.__client.parse_id_token(request, token)
        asid = self.get_asserted_subject_id(cs)
        try:
            sub = subjects.get(asid=asid)
        except subjects.DoesNotExist:
            sub = factory.new()
        sub.asid = asid
        sub.external = self.__external
        sub.is_superuser = self.is_superuser(cs)
        subjects.persist(sub)
        return sub

    def get_asserted_subject_id(self, cs):
        """Return the asserted subject identifier from the OAuth2 provider
        claims set.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def is_superuser(self, cs):
        """Return a boolean indicating if the :term:`Subject` asserted by
        the claims set is a superuser.
        """
        yes = False
        for superuser in self.__superusers:
            claim, value = str.split(superuser, ':')
            if cs.get(claim) != value:
                continue
            yes = True
            break
        return yes
