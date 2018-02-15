import unittest
import json
import os

from PyStacks.PyStacks.configs import loadConfig


class TestConfig(unittest.TestCase):

    def test_loadConfig_region_exist_file_not_expect_exception(self):
        with self.assertRaises(IOError):
            loadConfig(file_name='THISFILESHOULDNOTEXIST', region='aps2')

    def test_loadConfig_region_not_exist_expect_exception(self):
        with self.assertRaises(IOError):
            loadConfig(file_name='vpc', region='NOTREGION')

    def test_loadConfig_region_file_exist_expect_value(self):
        actual = loadConfig(file_name='vpc', region='aps2')
        self.assertIsNotNone(actual)

    def test_loadConfig_all_types(self):
        path = './PyStacks/configs/user/region/aps2/'
        types = [file_name.replace('.yml', '') for file_name in os.listdir(path) if file_name != 'environment.yml']
        types = [x for x in types if 'missing_stackname' not in x]

        for file_name in types:
            actual = loadConfig(file_name=file_name, region='aps2')
            self.assertIsNotNone(actual)
            self.assertTrue(len(json.dumps(actual)) > 50)

    def test_loadConfig_no_stack_name_exception(self):
        with self.assertRaises(ValueError) as err:
            loadConfig(file_name='missing_stackname_test', region='aps2')
        self.assertTrue(
            'Expected value "stackname" not in template' in str(err.exception))


if __name__ == '__main__':
    unittest.main()
