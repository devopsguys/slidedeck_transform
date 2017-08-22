import json
import copy
import sdt_common
import sdt_tag_parse


def get_all_tags_in_presentation(presentation):
    tags = []
    for slide in presentation.slides:
        if slide.has_notes_slide:
            text_frame = slide.notes_slide.notes_text_frame
            tags += get_all_tags_in_comment(text_frame.text)
    return sdt_common.uniq(tags)


def get_all_tags_in_comment(text):
    json_list = sdt_common.find_json_in_string(text)
    all_tags = []
    if json_list:
        for json_block in json_list:
            if sdt_common.is_json(json_block):
                json_data = json.loads(json_block)
                if 'tags' in json_data.keys():
                    tags = json_data['tags']
                    if not isinstance(tags, list):
                        tags = [tags]
                    all_tags += tags
    return sdt_common.uniq(all_tags)


def remove_json_from_comment(text):
    json_list = sdt_common.find_json_in_string(text)
    if json_list:
        for json_block in json_list:
            text = text.replace(json_block, "")
    return text


def delete_slide_if_tag_matches(presentation, index, slide, tags_to_delete):
    if slide.has_notes_slide:
        text_frame = slide.notes_slide.notes_text_frame
        tags_in_comment = sdt_tag_parse.get_all_tags_in_comment(
            text_frame.text)
        matching_tags = copy.copy(tags_in_comment)
        if sdt_common.should_delete_slide(tags_in_comment, tags_to_delete):
            print "Deleting slide {0} with matching tags '{1}'".format(index, matching_tags)
            sdt_common.delete_slide(presentation, slide)
        text_frame.text = sdt_tag_parse.remove_json_from_comment(
            text_frame.text)
