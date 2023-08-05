# pylint: disable=no-self-use,unused-argument,invalid-name
"""Declares :class:`BaseIdentityProviverRegistry`."""
import abc
import os
from collections import OrderedDict

import yaml


NOT_LOADED = object()


class BaseIdentityProviverRegistry(metaclass=abc.ABCMeta):
    """The base class for all identity provider registries."""
    provider_classes = abc.abstractproperty()
    resource_kind = abc.abstractproperty()
    schema_class = abc.abstractproperty()

    @property
    def secdir(self):
        """Returns the directory name holding the secrets (i.e. provider
        configurations) used by the :class:`BaseIdentityProviverRegistry`.
        """
        return os.path.join(self.__secdir, "iam.unimatrixone.io/providers")

    def __init__(self, *args, **kwargs):
        self.__providers = NOT_LOADED
        self.__schema = self.schema_class()
        self.__default = None
        self.__secdir = kwargs.get('secdir', os.getenv('APP_SECDIR'))

    def add(self, providers, resource):
        """Adds a new :term:`Identity Provider` to the registry
        dictionary `providers`.
        """
        providers[ resource['metadata']['name'] ] = self.get_provider(resource)
        return providers[ resource['metadata']['name'] ]

    def enabled(self):
        """Return a list containing all enabled providers."""
        if self.__providers == NOT_LOADED:
            self.load_providers()
        return list([x for x in self.__providers.values() if x.is_enabled()])

    def get_provider(self, resource):
        """Instantiate a new :class:`Provider` from the parameters
        specified in `resource`.
        """
        cls = self.get_provider_class(resource)
        args, kwargs = self.get_provider_args(resource)
        return cls.fromresource(resource, *args, **kwargs)

    def get_provider_args(self, resource):
        """Return the position and keyword arguments to instantiate
        a provider for this resource.
        """
        return [], {}

    def get_provider_class(self, resource):
        """Returns the provider implementation class for the given
        resource.
        """
        return self.provider_classes[ resource.get('type') ]

    def lookup(self, name):
        """Return the identity provider identified by `name`."""
        return self.__providers[name]

    def load_providers(self):
        """Load the providers of the specified :attr:`resource_kind` from
        the secrets directory.
        """
        providers = OrderedDict()
        for fn in os.listdir(self.secdir):
            fp = os.path.join(self.secdir, fn)
            for doc in yaml.load_all(open(fp), Loader=yaml.SafeLoader):
                if doc.get('kind') != self.resource_kind:
                    # Silently ignore unrecognized documents.
                    continue
                provider = self.add(providers, self.__schema.load(doc))
                if provider.is_default():
                    self.__default = provider

        self.__providers = providers

        # If there is no default provider at this point, select the first loaded
        # from the persistent configuration.
        if self.__default is None and bool(providers):
            self.__default = list(providers.values())[0]

    def get(self, name):
        """Return the identity provider identified by `name`. Load the providers
        from the persistent storage backend if not present.
        """
        if self.__providers == NOT_LOADED:
            self.load_providers()
        return self.lookup(name)

    def get_default_provider(self):
        """Return the default provider configured for this registry."""
        if self.__providers == NOT_LOADED:
            self.load_providers()
        return self.__default
