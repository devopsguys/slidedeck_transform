from PIL import Image, ImageChops
import sdt_common


def trim(image):
    background = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, background)
    diff = ImageChops.add(diff, diff, 1.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)


def update_logo(slide):
    for shape in slide.placeholders:
        if shape.name == "Picture Placeholder 3":
            idx = shape.placeholder_format.idx
            slide.shapes.add_picture(sdt_common.TEMP_LOGO_FILE,
                                     slide.placeholders[idx].left,
                                     slide.placeholders[idx].top,
                                     None,
                                     slide.placeholders[idx].height)
