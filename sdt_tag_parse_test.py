import unittest
import slidedeck_transform.sdt_tag_parse as sdt_tag_parse


class TestTagRecognition(unittest.TestCase):

    def test_no_tags(self):
        tags = sdt_tag_parse.get_all_tags_in_comment("")
        self.assertEqual(tags, [])

    def test_one_tag(self):
        tags = sdt_tag_parse.get_all_tags_in_comment(
            'ab{"tags": "tag1"}cd'
        )
        self.assertEqual(tags, ['tag1'])

    def test_list_of_tags(self):
        tags = sdt_tag_parse.get_all_tags_in_comment(
            'ab{"tags": ["tag1","tag2"]}cd'
        )
        self.assertEqual(tags, ['tag1', 'tag2'])

    def test_multiple_lists_of_tags(self):
        tags = sdt_tag_parse.get_all_tags_in_comment(
            'ab{"tags": ["tag1","tag2"]}blah{"tags": ["tag3","tag4"]}cd'
        )
        self.assertEqual(sorted(tags), ['tag1', 'tag2', 'tag3', 'tag4'])

    def test_a_list_and_a_single_tag(self):
        tags = sdt_tag_parse.get_all_tags_in_comment(
            'ab{"tags": ["tag1","tag2"]}blah{"tags": "tag3"}cd'
        )
        self.assertEqual(tags, ['tag1', 'tag2', 'tag3'])

    def test_invalid_json(self):
        tags = sdt_tag_parse.get_all_tags_in_comment(
            'ab{"tags": ["tag1","tag2"}cd'
        )
        self.assertEqual(tags, [])

    def test_valid_json_but_no_tags(self):
        tags = sdt_tag_parse.get_all_tags_in_comment(
            'ab{"bags": ["tag1","tag2"}cd')
        self.assertEqual(tags, [])


if __name__ == '__main__':
    unittest.main()
