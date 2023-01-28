import fitz
import subprocess
import re

from src.helpers import span_css, handle_indent
import pdb

class CReport:
    """A Congressional Report class"""

    def __init__(self, fname):
        """Create an instance of a CReport"""
        self.fname = fname
        self.doc = fitz.open(fname)

    def generate_cover_page(self, outfile=""):
        """The default cover page looks like crap, let's make it look like the first page of the PDF"""
        if outfile == "":
            outfile = self.fname.replace(".pdf", ".png")
        subprocess.check_call(
            [
                "mutool",
                "convert",
                "-F",
                "png",
                "-o",
                outfile,
                "-O",
                "width=600",
                self.fname,
                "1",
            ]
        )

    def replace_tables(self):
        """We know that the ePub chokes on tables, so let's maybe see if we can make them look pretty as a graphic?"""
        # https://codepen.io/vdavez/pen/WNKdVqr?editors=1111
        pass

    def generate_html(self):
        """The powerhouse of the CReport. Generate the html for a CReport
        
        Here's how this works. Each page has a bunch of blocks... Then:

        1. Loop through the blocks (think of them as divs). 
        2. Ignore divs that are hidden (i.e., have a white text color).
        3. Handle indentation and linebreaks for the first span in each line within the div
        4. Add in the styling for each span
        
        """
        elements = ["<!DOCTYPE html><html><body>"]

        # Generate the "front matter" of the html

        # Iterate through the pages
        for page in self.doc:
            blocks = page.get_text("dict", flags=fitz.TEXT_DEHYPHENATE)["blocks"]
            for block in blocks:
                block_html = ["<div>"]
                lines = block["lines"]
                first_span = block["lines"][0]["spans"][0]
                
                # Check if hidden text, and greedily ignore the whole div
                if first_span["color"] == 16777215:
                    continue

                # Check if page number
                if len(lines) == 1 and len(lines[0]["spans"]) == 1 and re.match(r"[\d|\s]+",first_span["text"]):
                    continue

                # Check if heading
                text = "".join([span["text"] for line in lines for span in line["spans"]])
                if text.isupper():
                    text=f"<h3>{text}</h3></div>"
                    block_html.append(text)
                    elements.append("".join(block_html))
                    continue

                # Otherwise, loop through lines
                for l_idx, line in enumerate(lines):
                    spans = line["spans"]


                    for s_idx, span in enumerate(spans):
                        text = span["text"]
                        if s_idx == 0:
                            # pdb.set_trace()

                            text = f"{handle_indent(block, l_idx, line['bbox'][0], span)}"

                        style = span_css(span)
                        block_html.append(f"<span style='{style}'>{text}</span>")
                    
                block_html.append("</div>")
                elements.append("".join(block_html))
        elements.append("</body></html>")
        with open('interim.html','w') as fname:
            fname.write(''.join(elements))

        return True

    def convert_to_epub(self):
        """Convert the html into an ePub"""
        pass
