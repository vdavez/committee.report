import fitz
import subprocess
import re
import base64

from src.helpers import span_css, handle_indent


class CReport:
    """A Congressional Report class"""

    def __init__(self, fname):
        """Create an instance of a CReport"""
        self.fname = fname
        self.doc = fitz.open(fname)
        self.generate_html()

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

    def replace_tables(self, page, b_idx, blocks):
        """We know that the ePub chokes on tables, so let's make them look pretty as a JPEG"""

        min_x = blocks[b_idx + 1]["bbox"][0]
        max_x = blocks[b_idx + 1]["bbox"][2]
        min_y = blocks[b_idx]["bbox"][1]
        max_y = blocks[b_idx + 1]["bbox"][3]

        clip = (min_x, min_y, max_x, max_y)
        zoom = 600 / (max_x - min_x)
        mat = fitz.Matrix(zoom, zoom)

        pix = page.get_pixmap(matrix=mat, clip=clip)
        stream = pix.pil_tobytes(format="JPEG", quality=100)
        img_data_url = "data:image/jpeg;base64," + base64.b64encode(stream).decode()
        return f"<img src='{img_data_url}' width=600 style='padding: 1em 1em'/>"

    def generate_html(self):
        """The powerhouse of the CReport. Generate the html for a CReport

        Here's how this works. Each page has a bunch of blocks... Then:

        1. Loop through the blocks (think of them as divs).
        2. Ignore divs that are hidden (i.e., have a white text color).
        3. Handle indentation and linebreaks for the first span in each line within the div
        4. Add in the styling for each span

        """

        vote = 0

        # Generate the "front matter" of the html
        elements = [
            "<!DOCTYPE html><html><head><style>div{line-height:normal}</style><body>"
        ]

        # Iterate through the pages
        for page in self.doc:
            blocks = page.get_text("dict", flags=fitz.TEXT_DEHYPHENATE)["blocks"]
            for b_idx, block in enumerate(blocks):
                lines = block["lines"]
                first_span = block["lines"][0]["spans"][0]

                # Check if hidden text, and greedily ignore the whole div
                if first_span["color"] == 16777215:
                    continue

                # Check if page number
                if (
                    len(lines) == 1
                    and len(lines[0]["spans"]) == 1
                    and re.match(r"[\d|\s]+", first_span["text"])
                ):
                    continue

                block_html = ["<div>"]

                # Check if heading
                text = "".join(
                    [span["text"] for line in lines for span in line["spans"]]
                )
                if text.isupper():
                    text = f"<h3>{text}</h3></div>"
                    block_html.append(text)
                    elements.append("".join(block_html))
                    continue

                # Check if it's a vote
                if text == "Majority Members Vote Minority Members Vote ":
                    img_elem = self.replace_tables(page, b_idx, blocks)
                    vote = 1
                    elements.append(img_elem)
                    continue
                if vote == 1:
                    vote = 0
                    continue

                # Otherwise, loop through lines
                for l_idx, line in enumerate(lines):
                    spans = line["spans"]

                    for s_idx, span in enumerate(spans):
                        text = span["text"]
                        if s_idx == 0:
                            text = (
                                f"{handle_indent(block, l_idx, line['bbox'][0], span)}"
                            )

                        style = span_css(span)
                        block_html.append(f"<span style='{style}'>{text}</span>")

                block_html.append("</div>")
                elements.append("".join(block_html))
        elements.append("</body></html>")
        self.html = "".join(elements)
        return True
