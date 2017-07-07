import regex


def find_templates_in_string(text):
    templates = regex.findall('{{.*?}}', text)

    def strip_brackets(x):
        return x[2:-2]

    return list(map(strip_brackets, templates))
