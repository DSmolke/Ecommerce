import unittest
from ecomerceapp.common.utils import get_n_top_elements_of_most_common_list

class TestGetNElementOfMostCommonList(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.with_one_most_common = [('a', 5), ('b', 4), ('c', 3)]
        cls.with_two_most_common = [('a', 5), ('b', 5), ('c', 3)]
        cls.with_all_three_most_common = [('a', 5), ('b', 5), ('c', 5)]
        cls.empty_list = []
        cls.one_element_list = [('a', 5)]

    def test_one_most_common(self):
        self.assertEqual(get_n_top_elements_of_most_common_list(self.with_one_most_common), 1)

    def test_two_most_common(self):
        self.assertEqual(get_n_top_elements_of_most_common_list(self.with_two_most_common), 2)

    def test_all_three_most_common(self):
        self.assertEqual(get_n_top_elements_of_most_common_list(self.with_all_three_most_common), 3)

    def test_empty_list_case(self):
        with self.assertRaises(IndexError) as e:
            get_n_top_elements_of_most_common_list(self.empty_list)
        self.assertEqual("List is empty therefor index will be invalid", str(e.exception))

    def test_list_with_one_element_case(self):
        self.assertEqual(get_n_top_elements_of_most_common_list(self.one_element_list), 1)


if __name__ == "__main__":
    unittest.main()
