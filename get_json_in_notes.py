import sys
import json
from pptx import Presentation
from pptx.util import Inches, Pt

def delete_slide(prs, slide):
    #Make dictionary with necessary information
    id_dict = {slide.id: [i, slide.rId] for i, slide in enumerate(prs.slides._sldIdLst)}
    slide_id = slide.slide_id
    prs.part.drop_rel(id_dict[slide_id][1])
    del prs.slides._sldIdLst[id_dict[slide_id][0]]

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

PRS = Presentation(sys.argv[1])

width = height = Inches(1)
left = top = Inches(2)

for slide in PRS.slides:
    # logo_image = "/Users/edmundd/Desktop/logo_gb.png"
    logo_image = "/Users/edmundd/Desktop/Nokia-logo.jpg"
    # logo_image = "/Users/edmundd/Desktop/logo.gif"
    

    for shape in slide.placeholders:
        if shape.name == "Picture Placeholder 3":
            idx = shape.placeholder_format.idx
            pic = slide.shapes.add_picture(logo_image, left, slide.placeholders[idx].top, None, slide.placeholders[idx].height)

    if slide.has_notes_slide:
        text_frame = slide.notes_slide.notes_text_frame
        try:
            metadata = json.loads(text_frame.text)
            if "hello" in metadata['tags']:
                delete_slide(PRS, slide)
        except:
            pass

PRS.save('/Users/edmundd/Desktop/Test Presentation2.pptx')
