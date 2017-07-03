import sys
import json
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from PIL import Image, ImageChops
import regex

TEMP_LOGO_FILE = "temp_logo.png"

def get_tags_in_comments(text):
    jsons = find_json_in_string(text)
    tags = []
    return tags

def find_json_in_string(text):
    return regex.findall('{(?:[^{}]|(?R))*}', text)

def trim(image):
    background = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, background)
    diff = ImageChops.add(diff, diff, 1.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)

def delete_slide(prs, slide):
    #Make dictionary with necessary information
    id_dict = {slide.id: [i, slide.rId] for i, slide in enumerate(prs.slides._sldIdLst)}
    slide_id = slide.slide_id
    prs.part.drop_rel(id_dict[slide_id][1])
    del prs.slides._sldIdLst[id_dict[slide_id][0]]

def main():

    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    PRS = Presentation(sys.argv[1])

    width = height = Inches(1)
    left = top = Inches(2)

    for slide in PRS.slides:
        logo_image = "/Users/edmundd/Desktop/logo_gb.png"
        # logo_image = "/Users/edmundd/Desktop/Nokia-logo.jpg"
        # logo_image = "/Users/edmundd/Desktop/logo.gif"
        
        # trim(Image.open(logo_image)).save(TEMP_LOGO_FILE)

        Image.open(logo_image).save(TEMP_LOGO_FILE)

        for shape in slide.placeholders:
            if shape.name == "Picture Placeholder 3":
                idx = shape.placeholder_format.idx
                pic = slide.shapes.add_picture(TEMP_LOGO_FILE, left, slide.placeholders[idx].top, None, slide.placeholders[idx].height)

        if slide.has_notes_slide:
            text_frame = slide.notes_slide.notes_text_frame
            try:
                metadata = json.loads(text_frame.text)
                if "hello" in metadata['tags']:
                    delete_slide(PRS, slide)
            except:
                pass
        
        os.remove(TEMP_LOGO_FILE) 

    PRS.save('/Users/edmundd/Desktop/Test Presentation2.pptx')
