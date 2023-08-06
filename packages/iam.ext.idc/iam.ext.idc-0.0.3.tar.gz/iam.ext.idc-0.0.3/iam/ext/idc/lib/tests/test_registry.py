# pylint: skip-file
import unittest
from collections import defaultdict

import marshmallow
import marshmallow.fields
import unimatrix.lib.test

from ..registry import BaseIdentityProviverRegistry


class default_provider_class:

    @classmethod
    def fromresource(cls, *args, **kwargs):
        return cls()


class typed_provider_class(default_provider_class):
    pass


@unimatrix.lib.test.unit
class BaseIdentityProviverRegistryTestCase(unittest.TestCase):

    class impl_class(BaseIdentityProviverRegistry):
        provider_classes = defaultdict(
            lambda: default_provider_class,
            {'test': typed_provider_class}
        )
        resource_kind = 'TestProvider'

        class schema_class(marshmallow.Schema):
            kind = marshmallow.fields.String(required=True)
            metadata = marshmallow.fields.Dict()

    def setUp(self):
        self.impl = self.impl_class()

    def test_get_provider_class_returns_default_without_type(self):
        cls = self.impl.get_provider_class({})
        self.assertEqual(cls, default_provider_class)

    def test_get_provider_class_returns_type(self):
        cls = self.impl.get_provider_class({'type': 'test'})
        self.assertEqual(cls, typed_provider_class)

    def test_add_updates_providers(self):
        providers = {}
        self.impl.add(providers, {
            'kind': self.impl_class.resource_kind,
            'metadata': {
                'name': 'foo'
            }
        })
        self.assertIn('foo', providers)

    def test_get_provider_args_defaults_to_empty(self):
        args, kwargs = self.impl.get_provider_args({})
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {})

    def get_provider_returns_instance(self):
        provider = self.impl.get_provider({
            'kind': self.impl_class.resource_kind,
            'metadata': {
                'name': 'foo'
            }
        })
        self.assertIsInstance(provider, default_provider_class)
