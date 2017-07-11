import argparse
import json
from pptx import Presentation
import sdt_tag_parse
import sdt_string_replace


def parse_args():
    parser = argparse.ArgumentParser(
        description='List tags')
    required = parser.add_argument_group('Required arguments')
    optional = parser.add_argument_group('Optional arguments')
    required.add_argument('--file', nargs=1, action='store',
                          help="Path to the powerpoint presentation file")

    return parser.parse_args()


def main():
    ARGS = parse_args()
    presentation_file = ARGS.file[0]
    presentation = Presentation(presentation_file)
    all_tags = sdt_tag_parse.get_all_tags_in_presentation(presentation)
    all_template_strings = sdt_string_replace.find_all_template_strings_in_presentation(
        presentation)

    print json.dumps({"tags": all_tags, "templates": all_template_strings})


if __name__ == '__main__':
    main()
