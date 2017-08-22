import regex
import sdt_common


def strip_brackets(x):
    return x[2:-2].strip().lower()


def find_templates_in_string(text):
    templates = regex.findall('{{.*?}}', text)

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
