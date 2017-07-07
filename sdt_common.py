import json
import regex

TEMP_LOGO_FILE = "temp_logo.png"


def uniq(items):
    return list(set(items))


def is_json(text):
    try:
        json.loads(text)
    except ValueError:
        return False
    return True


def find_json_in_string(text):
    return regex.findall('{(?:[^{}]|(?R))*}', text)


def delete_slide(prs, slide):
    # Make dictionary with necessary information
    id_dict = {slide.id: [i, slide.rId]
               for i, slide in enumerate(prs.slides._sldIdLst)}
    slide_id = slide.slide_id
    prs.part.drop_rel(id_dict[slide_id][1])
    del prs.slides._sldIdLst[id_dict[slide_id][0]]


def should_delete_slide(tags_in_comment, tags_to_delete):
    if tags_in_comment != []:
        for tag in tags_to_delete:
            if tag in tags_in_comment:
                tags_in_comment.remove(tag)
        return tags_in_comment == []
    return False
