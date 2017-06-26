import sys
import json
from pptx import Presentation

def delete_slide(prs, slide):
    #Make dictionary with necessary information
    id_dict = { slide.id: [i, slide.rId] for i,slide in enumerate(prs.slides._sldIdLst) }
    slide_id = slide.slide_id
    prs.part.drop_rel(id_dict[slide_id][1])
    del prs.slides._sldIdLst[id_dict[slide_id][0]]

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

prs = Presentation(sys.argv[1])

for slide in prs.slides:
    if(slide.has_notes_slide):
        text_frame = slide.notes_slide.notes_text_frame
        print text_frame.text
        try:
            metadata = json.loads(text_frame.text)
            if("hello" in metadata['tags']):
                delete_slide(prs,slide)
        except:
            pass

prs.save('/Users/edmundd/Desktop/Test Presentation2.pptx')