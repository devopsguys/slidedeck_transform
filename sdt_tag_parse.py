import json
import common as sl_common


def get_all_tags_in_presentation(presentation):
    tags = []
    for slide in presentation.slides:
        if slide.has_notes_slide:
            text_frame = slide.notes_slide.notes_text_frame
            tags += get_all_tags_in_comment(text_frame.text)
    return sl_common.uniq(tags)


def get_all_tags_in_comment(text):
    json_list = sl_common.find_json_in_string(text)
    all_tags = []
    if json_list:
        for json_block in json_list:
            if sl_common.is_json(json_block):
                tags = json.loads(json_block)['tags']
                if not isinstance(tags, list):
                    tags = [tags]
                all_tags += tags
    return sl_common.uniq(all_tags)


def remove_json_from_comment(text):
    json_list = sl_common.find_json_in_string(text)
    if json_list:
        for json_block in json_list:
            text = text.replace(json_block, "")
    return text
