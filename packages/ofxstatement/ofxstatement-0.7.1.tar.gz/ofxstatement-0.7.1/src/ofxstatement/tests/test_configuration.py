import os
import unittest

from ofxstatement import configuration
from ofxstatement.exceptions import Abort


class ConfigurationTest(unittest.TestCase):
    def test_configuration(self) -> None:
        here = os.path.dirname(__file__)
        cfname = os.path.join(here, "samples", "config.ini")
        config = configuration.read(cfname)
        assert config is not None
        self.assertEqual(config["swedbank"]["plugin"], "swedbank")

    def test_default_configuration(self) -> None:
        default_config = configuration.read(configuration.get_default_location())
        config = configuration.read()
        self.assertEqual(config, default_config)

    def test_missing_configuration(self) -> None:
        config = configuration.read("missing.ini")
        self.assertIsNone(config)

    def test_missing_section(self) -> None:
        here = os.path.dirname(__file__)
        cfname = os.path.join(here, "samples", "config.ini")
        config = configuration.read(cfname)
        with self.assertRaises(Abort):
            configuration.get_settings(config, "kawabanga")
