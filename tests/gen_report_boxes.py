import fitz 

doc = fitz.open('tests/test_report.pdf')

for page in doc:
    for block in page.get_text("dict", flags=fitz.TEXT_DEHYPHENATE)["blocks"]:
        page.draw_rect(fitz.Rect(block["bbox"]))
        for line in block["lines"]:
            page.draw_rect(fitz.Rect(line["bbox"]), color=(1,0,0))

doc.save("tests/test_report_boxes.pdf")