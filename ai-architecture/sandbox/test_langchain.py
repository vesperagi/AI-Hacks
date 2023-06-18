import unittest
from langchain_test import determine_health_use

class MyTestCase(unittest.TestCase):
    def test_determinator(self):
        test = determine_health_use("can you do a quick recap of the report you gave me yesterday?") # health database == true
        self.assertEqual("false", test)  # add assertion here


if __name__ == '__main__':
    unittest.main()
