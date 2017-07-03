import unittest
import slidedeck_transform.tag_recognition

class TestTagRecognition(unittest.TestCase):

    def test_no_tags_in_comments(self):
        tags = slidedeck_transform.tag_recognition.get_tags_in_comments("")
        self.assertEqual(tags, [])

    def test_one_tag_in_comments(self):
        tags = slidedeck_transform.tag_recognition.get_tags_in_comments('{"tags": "tag1"}')
        self.assertEqual(tags, ['tag1'])

    def test_list_of_tags_in_comments(self):
        tags = slidedeck_transform.tag_recognition.get_tags_in_comments('{"tags": ["tag1","tag2"]}')
        self.assertEqual(tags, ['tag1', 'tag2'])


if __name__ == '__main__':
    unittest.main()
