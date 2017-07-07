import regex


def find_templates_in_string(text):
    templates = regex.findall('{{.*?}}', text)

    def strip_brackets(x):
        return x[2:-2]

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
    return templates
