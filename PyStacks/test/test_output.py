import unittest
from hypothesis import given
from hypothesis.strategies import text

from PyStacks.PyStacks.output import boxwrap
from PyStacks.PyStacks.output import writecolour
from PyStacks.PyStacks.output import whalesay
from PyStacks.PyStacks.output import piesay


class TestOutput(unittest.TestCase):

    def test_boxwrap(self):
        result = boxwrap('this is some text')
        self.assertEqual(result, '+------------------------+\n| 1. this is some text   |\n+------------------------+')

    def test_boxwrap_nolinenos(self):
        result = boxwrap('this is some text', linenumbers=False)
        self.assertEqual(result, '+--------------------+\n| this is some text  |\n+--------------------+')

    def test_whalesay(self):
        result = whalesay('Whale, whale whale, whats all this then?')
        self.assertTrue('+\n| Whale, whale whale, whats all this then?  |\n+' in result)

    def test_piesay(self):
        result = piesay('A stack of pies')
        self.assertTrue('stack of pies' in result)

    def test_colour(self):
        result = writecolour('VGVycnkgd2FzIGhlcmU=')
        self.assertTrue('VGVycnkgd2FzIGhlcmU=' in result)

    @given(text())
    def test_decode_inverts_encode(self, s):
        assert '""""""""""""""""' in whalesay(s)


if __name__ == '__main__':
    unittest.main()
