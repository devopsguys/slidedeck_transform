import regex
import sdt_common
import json


def strip_brackets(x):
    return x[2:-2].strip().lower()


def find_templates_in_string(text):
    templates = regex.findall('{{.*?}}', text)

    return list(map(strip_brackets, templates))


def find_all_template_strings_in_presentation(presentation):

    template_names = []
    templates = []

    for slide in presentation.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            text_frame = shape.text_frame
            for paragraph in text_frame.paragraphs:
                for template in find_templates_in_string(paragraph.text):
                    template_names += [template]
    for template in sdt_common.uniq(template_names):
        templates.append(
            {"name": template, "default": get_template_default(template, presentation)})
    return templates


def get_template_default(name, presentation):
    first_slide = presentation.slides[0]

    if first_slide.has_notes_slide:
        text = first_slide.notes_slide.notes_text_frame.text
        json_list = sdt_common.find_json_in_string(text)
        if json_list:
            for json_block in json_list:
                if sdt_common.is_json(json_block):
                    json_data = json.loads(json_block)
                    if json_data.get('defaults', {}).get(name):
                        return json_data['defaults'][name]
    return ""


def replace_template_string(slide, template, text):
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        text_frame = shape.text_frame
        for paragraph in text_frame.paragraphs:
            for template_placeholder in regex.findall('{{.*?}}', paragraph.text):
                if strip_brackets(template_placeholder) == template:
                    replace_paragraph_text_retaining_initial_formatting(paragraph, paragraph.text.replace(
                        template_placeholder, text))


def replace_paragraph_text_retaining_initial_formatting(paragraph, new_text):
    p = paragraph._p  # the lxml element containing the `<a:p>` paragraph element
    # remove all but the first run
    for idx, run in enumerate(paragraph.runs):
        if idx == 0:
            continue
        p.remove(run._r)
    paragraph.runs[0].text = new_text
