import unittest
import slidedeck_transform.sdt_common as sdt_common


class TestCommonFunctions(unittest.TestCase):

    def test_is_json_detection(self):
        self.assertTrue(sdt_common.is_json("{}"))
        self.assertFalse(sdt_common.is_json("{!}"))
