import unittest
import data_tree
from hypothesis import strategies, given, settings
import logging
import string

logging.basicConfig()
logging.setLevel('DEBUG')

logger = logging.getLogger('DATATREETEST')

class DataTreeTest(unittest.TestCase):
    @settings(min_satisfying_examples=10, max_examples=50, timeout=10)
    @given(letter_1 = strategies.text( alphabet=string.printable, min_size=1, max_size=1),
           letter_2 = strategies.text( alphabet=string.printable, min_size=1, max_size=1))
    def test_no_dupes(self, letter_1, letter_2):
        dt = data_tree.DataTree()
        dt.add_data(None, letter_1)
        self.assertRaises(IndexError, dt.add_data, (None, letter_1))
        if letter_1 == letter_2:
            self.assertRaises(IndexError, dt.add_data, (None, letter_2))

    @given( letters = [strategies.text( alphabet=string.ascii_uppercase, min_size=1, max_size=1) for i in range(8)] )
    def test_combine_trees(self, letters):
        dt_1, dt_2 = data_tree.DataTree(), data_tree.DataTree()
        dt_1.add_data(None, letters[0])
        dt_1.add_data(None, letters[1])
        dt_1.add_data(letters[0], letters[2])
        dt_1.add_data(letters[0], letters[3])
        dt_2.add_data(None, letters[4])
        dt_2.add_data(letters[4], letters[5])
        dt_2.add_data(letters[4], letters[6])
        dt_2.add_data(letters[6], letters[7])
        self._logger.debug(dt_1)
        self._logger.debug(dt_2)
        dt_1+dt_2

if __name__ in "__main__":
    unittest.main()