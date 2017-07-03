import unittest
import slidedeck_transform.tag_recognition


class TestTagRecognition(unittest.TestCase):

    def test_is_json_detection(self):
        self.assertTrue(slidedeck_transform.tag_recognition.is_json("{}"))
        self.assertFalse(slidedeck_transform.tag_recognition.is_json("{!}"))

    def test_no_tags(self):
        tags = slidedeck_transform.tag_recognition.get_tags_in_comments("")
        self.assertEqual(tags, [])

    def test_one_tag(self):
        tags = slidedeck_transform.tag_recognition.get_tags_in_comments(
            'ab{"tags": "tag1"}cd'
        )
        self.assertEqual(tags, ['tag1'])

    def test_list_of_tags(self):
        tags = slidedeck_transform.tag_recognition.get_tags_in_comments(
            'ab{"tags": ["tag1","tag2"]}cd'
        )
        self.assertEqual(tags, ['tag1', 'tag2'])

    def test_multiple_lists_of_tags(self):
        tags = slidedeck_transform.tag_recognition.get_tags_in_comments(
            'ab{"tags": ["tag1","tag2"]}blah{"tags": ["tag3","tag4"]}cd'
        )
        self.assertEqual(tags, ['tag1', 'tag2', 'tag3', 'tag4'])

    def test_a_list_and_a_single_tag(self):
        tags = slidedeck_transform.tag_recognition.get_tags_in_comments(
            'ab{"tags": ["tag1","tag2"]}blah{"tags": "tag3"}cd'
        )
        self.assertEqual(tags, ['tag1', 'tag2', 'tag3'])

    def test_invalid_json(self):
        tags = slidedeck_transform.tag_recognition.get_tags_in_comments(
            'ab{"tags": ["tag1","tag2"}cd'
        )
        self.assertEqual(tags, [])

    def test_valid_json_but_no_tags(self):
        tags = slidedeck_transform.tag_recognition.get_tags_in_comments(
            'ab{"bags": ["tag1","tag2"}cd')
        self.assertEqual(tags, [])


if __name__ == '__main__':
    unittest.main()
