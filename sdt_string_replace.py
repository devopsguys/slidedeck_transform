import regex
import sdt_common


def find_templates_in_string(text):
    templates = regex.findall('{{.*?}}', text)

    def strip_brackets(x):
        return x[2:-2].strip()

    return list(map(strip_brackets, templates))


def find_all_template_strings_in_presentation(presentation):
    templates = []
    for slide in presentation.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            text_frame = shape.text_frame
            for paragraph in text_frame.paragraphs:
                for template in find_templates_in_string(paragraph.text):
                    templates += [template]
    return sdt_common.uniq(templates)


def replace_template_string(slide, template, text):
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        text_frame = shape.text_frame
        for paragraph in text_frame.paragraphs:
            if "{{{0}}}".format(template) in paragraph.text:
                paragraph.text = paragraph.text.replace(
                    '{{' + template + '}}', text)
