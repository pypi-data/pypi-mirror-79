# pylint: disable=invalid-name,no-self-use
"""Declares :class:`OAuth2Ctrl`."""
import functools
import time
import uuid

from authlib.integrations.django_client import OAuth
from django.http import JsonResponse
from django.middleware.csrf import rotate_token
from django.urls import include
from django.urls import reverse
from django.urls import path

from iam.ext.idc.lib.oauth2.registry import OAuth2ProviderRegistry


class OAuth2Ctrl:
    """Controllers for all OAuth2 provider endpoints."""

    @property
    def urlpatterns(self):
        """Return the list of URL patterns exposed by :class:`OAuth2Ctrl`."""
        return ([
            path('login', self.login_using_default,
                name='login_default'),
            path('providers/default', self.get_default_provider,
                name='providers.default'),
            path('providers', self.list_providers,
                name='providers'),
            path('<str:using>/authorize', self.inject_provider(self.authorize),
                name='authorize'),
            path('<str:using>/login', self.inject_provider(self.login),
                name='login'),
        ], 'idc')

    @classmethod
    def as_namespace(cls, base_path, namespace='oauth2'):
        """Instantiate a :class:`OAuth2Ctrl` instance and return an iterable
        suitable for use with :func:`django.urls.include`.

        Args:
            base_path (str): the base path to mount the OAuth2 URL to. Must not
                include a leading slash.
            namespace (str): the URL namespace. Defaults to ``oauth2``.

        Returns:
            iterable
        """
        ctrl = cls(OAuth2ProviderRegistry(OAuth()), namespace=namespace)
        return path(base_path, include(ctrl.urlpatterns, namespace=namespace))

    def inject_provider(self, func):
        """Decorate `func` so that the provider is injected based on the
        `using` URL parameter.
        """
        @functools.wraps(func)
        def f(request, using, *args, **kwargs):
            try:
                return func(request, self.registry.get(using), *args, **kwargs)
            except KeyError:
                list_url = self.get_enabled_providers_uri(request)
                dto = {
                    'id': str(uuid.uuid4()),
                    'timestamp': int(time.time() * 1000),
                    'code': "IDENTITY_PROVIDER_DOES_NOT_EXIST",
                    'message': f"The selected identity provider '{using}' does not exist.",
                    'hint': f"Inspect {list_url} for a list of enabled identity providers.",
                    'audit': {
                        'message': "This error is recorded along with your IP address."
                    }
                }
                return JsonResponse(dto, status=404,
                    json_dumps_params={'indent': 2})

        return f

    def __init__(self, registry, namespace):
        self.registry = registry
        self.namespace = namespace

    def authorize(self, request, provider):
        """Invoked when the user is redirected by the SSO provider after the
        authentication dialog.
        """
        subject = provider.get_asserted_subject(request)
        if subject is not None:
            provider.login(request,subject)
        else:
            raise NotImplementedError
        return JsonResponse({'asid': subject.asid},
            json_dumps_params={'indent': 2})

    def get_authorize_uri(self, request, using): # pylint: disable=unused-argument
        """Return the absolute URL to which the :term:`Asserting Party` must
        redirect after the login dialog.
        """
        return reverse(f'{self.namespace}:authorize', kwargs={'using': using})

    def get_default_provider(self, request):
        """Return a JSON response containing the default OAuth2 provider."""
        provider = self.registry.get_default_provider()
        return JsonResponse({
            'description': provider.description,
            'loginUrl': self.get_login_uri(request, provider.name)
            }, json_dumps_params={'indent': 2})

    def get_enabled_providers_uri(self, request):
        """Return URL yielding the enabled providers."""
        return request.build_absolute_uri(reverse(f'{self.namespace}:providers'))

    def get_login_uri(self, request, using):
        """Return the login URL for the given provider."""
        return request.build_absolute_uri(
            reverse(f'{self.namespace}:login', kwargs={'using': using}))

    def list_providers(self, request):
        """Return a JSON response containing the enabled OAuth2 providers."""
        return JsonResponse({
            'providers': [{
            'description': x.description,
            'loginUrl': self.get_login_uri(request, x.name)
        } for x in self.registry.enabled()]}, json_dumps_params={'indent': 2})

    def login(self, request, provider):
        """Redirect the client to the OAuth2 provider login screen."""
        rotate_token(request)
        return provider.authorize_redirect(request,
            request.build_absolute_uri(self.get_authorize_uri(request, provider.name)))

    def login_using_default(self, request):
        """Login using the default provider."""
        return self.login(request, self.registry.get_default_provider())
