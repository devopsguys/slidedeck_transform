import unittest
import slidedeck_transform.sdt_common as sdt_common


class TestCommonFunctions(unittest.TestCase):

    def test_is_json_detection(self):
        self.assertTrue(sdt_common.is_json("{}"))
        self.assertFalse(sdt_common.is_json("{!}"))

    def test_should_delete_slide(self):
        self.assertFalse(sdt_common.should_delete_slide(['a', 'b'], ['c']))
        self.assertTrue(sdt_common.should_delete_slide(
            ['a', 'b', 'c'], ['c', 'd']))
