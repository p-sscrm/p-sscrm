# json2docx.py - quick script to generate Markdown document to be fed to pandoc -f docx, for P-SSCRM practices and tasks defined in p-sscrm-1_0.json
# This probably should take arguments, e.g. the json file, an optional practice or task name, a directory in which to store the results

import json
from docx import Document 
from docx.shared import Pt

def make_group(doc,g,hlevel):
    doc.add_heading(g['id'] + " " + g['name'],hlevel)
    doc.add_heading('Description',hlevel+1)
    doc.add_paragraph(g['description'])

    doc.add_heading('Practices',hlevel+1)
    for p in g['practices']:
        doc.add_paragraph(p['id'] + " " + p['name'])
    doc.add_page_break()

def make_practice(doc,p,hlevel):
    doc.add_heading(p['id'] + " " + p['name'],hlevel)
    doc.add_heading('Description',hlevel+1)
    doc.add_paragraph(p['description'])
    doc.add_page_break()

def make_task(doc,t,hlevel):
    doc.add_heading(t['id'] + " " + t['name'],hlevel)
    doc.add_heading('Objective',hlevel+1)
    doc.add_paragraph(t['objective'])
    doc.add_heading('Definition',hlevel+1)
    doc.add_paragraph(t['definition'])
    doc.add_heading('Questions',hlevel+1)
    for q in t['questions']:
        doc.add_heading(q['id'] + " " + q['text'],hlevel+2)
        paragraph = doc.add_paragraph("")
        paragraph.paragraph_format.space_after = Pt(200)


def main():
    jfilename = "data/p-sscrm-2_0.json"
    ofilename = "psscrm_oe.docx"
    j = json.load(open(jfilename))

    document = Document()
    hlevel = 0
    document.add_heading('PSSCRM OE',hlevel)
    document.add_paragraph("This document is the Open-Ended (OE) version of the P-SSCRM assessment tool.")
    for g in j['groups']:
        make_group(document,g,hlevel+1)
        for p in g['practices']:
            make_practice(document,p,hlevel+2)
            for t in p['tasks']:
                print("Task: ", t['name'],t['id'])
                make_task(document,t,hlevel+3)
    document.save("artifacts/" + ofilename)
if __name__ == '__main__':
    main()      
