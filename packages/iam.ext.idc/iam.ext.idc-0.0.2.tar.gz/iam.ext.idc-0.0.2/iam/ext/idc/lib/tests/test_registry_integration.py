# pylint: skip-file
import os
import tempfile
import unittest
from collections import defaultdict

import marshmallow
import marshmallow.fields
import unimatrix.lib.test

from ..registry import BaseIdentityProviverRegistry
from ..provider import BaseProvider


TEST_PROVIDERS = """
---
kind: MockProvider
metadata:
  name: test1
spec:
  default: false
---
kind: MockProvider
metadata:
  name: test2
spec:
  default: true
---
kind: MockProvider
metadata:
  name: test3
spec:
  default: true
  enabled: false
---
kind: OtherProvider
metadata:
  name: test4
"""


@unimatrix.lib.test.integration
class BaseIdentityProviverRegistryTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.secdir = tempfile.mkdtemp()
        os.makedirs(os.path.join(cls.secdir, 'iam.unimatrixone.io/providers'))

        cls.fp = os.path.join(cls.secdir,
            "iam.unimatrixone.io/providers", 'providers.yaml')
        with open(cls.fp, 'w') as f:
            f.write(TEST_PROVIDERS)

    def setUp(self):
        self.registry = MockRegistry(secdir=self.secdir)

    def test_load_from_disk(self):
        self.registry.load_providers()

    def test_enabled_shows_correct_number(self):
        self.assertEqual(len(self.registry.enabled()), 2)

    def test_get_provider_returns_named_provider(self):
        provider = self.registry.get('test1')

    def test_get_default_provider_returns_specified(self):
        provider = self.registry.get_default_provider()
        self.assertEqual(provider.resource['metadata']['name'], 'test3')

    def test_no_default_picks_first(self):
        fp = os.path.join(self.secdir,
            "iam.unimatrixone.io/providers", 'providers.yaml')
        with open(fp, 'w') as f:
            f.write(str.replace(TEST_PROVIDERS, 'default: true', 'default: false'))
        registry = MockRegistry(secdir=self.secdir)
        provider = registry.get_default_provider()
        self.assertEqual(provider.resource['metadata']['name'], 'test1')
    

class MockProvider(BaseProvider):

    @classmethod
    def fromresource(cls, resource):
        return cls(resource)

    def __init__(self, resource):
        self.resource = resource

    def is_default(self):
        return bool(self.resource['spec'].get('default'))

    def is_enabled(self):
        return bool(self.resource['spec'].get('enabled', True))


class MockRegistry(BaseIdentityProviverRegistry):
    provider_classes =  defaultdict(lambda: MockProvider)
    resource_kind = 'MockProvider'

    class schema_class(marshmallow.Schema):
        kind = marshmallow.fields.String(required=True)
        metadata = marshmallow.fields.Dict()
        spec = marshmallow.fields.Dict()
