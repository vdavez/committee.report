import fitz
import json
doc = fitz.open('tests/test_report.pdf')
fname = open('test_blocks.json','w')
blocks = []
for page in doc: 
    blocks.append(page.get_text('dict', flags=fitz.TEXT_DEHYPHENATE)['blocks'])

with open('tests/test_blocks.json', 'w') as jsonfile:
    json.dump(blocks, jsonfile)