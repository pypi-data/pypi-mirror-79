from wedge.tests.builders.abstract_test_builder import AbstractTestBuilder
from wedge.tests.fixtures.datasets.builders.factory_boy import SimpleExampleFactory


class SimpleBuilder(AbstractTestBuilder):
    _factories = {"example": SimpleExampleFactory}
    _main_factory_key = "example"
