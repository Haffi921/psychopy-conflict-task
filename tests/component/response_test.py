import unittest

from conflict_task.component import ResponseComponent

response = dict(
    start = 1.3,
    stop = 3.0,
)

keys = ["a", "b", "c", "d"]

class TestResponseCreation(unittest.TestCase):

    def test_response_has_no_keys(self):
        with self.assertRaises(SystemExit):
            ResponseComponent(response)


    def test_response_has_keys_of_no_length(self):
        response["keys"] = []
        with self.assertRaises(SystemExit):
            ResponseComponent(response)
    

    def test_response_has_valid_keys(self):
        response["keys"] = keys
        r = ResponseComponent(response)
        self.assertEqual(r.keys, keys)

if __name__ == '__main__':
    unittest.main()