def handle_indent(block, l_idx, l_bbox_x, span, char=5, min_x=147):
    """Check to see if a span's bbox is greater than the block's bbox. If it is, add an indent"""

    b0 = block["bbox"][0]
    b1 = span["origin"][0]

    chars = ""

    # Check to see if it's legislative text or a list...
    if span["text"][0] == "(" or span["text"][0] == "—":
        chars = "<br>" + int((b1 - min_x) / char) * "&nbsp;"

    # If it's the first line in the block and indented...
    elif l_idx == 0 and b1 > b0:
        chars = "<br>" + int((b1 - min_x) / char) * "&nbsp;"

    # HACKY ALERT! If it's the the span has text size of 10 and indented...
    elif (
        span["size"] == 10
        and span["font"] == "NewCenturySchlbk-Roman"
        and b1 > b0
        and l_bbox_x == b0
    ):
        chars = "<br>" + int((b1 - min_x) / char) * "&nbsp;"

    text = chars + span["text"]
    return text


def add_redaction(page, span):
    """Check if white text, add redaction"""
    if span["color"] == 16777215:
        annot = page.add_redact_annot(fitz.Rect(span["bbox"]), fill=True)
    return True


def scale_size(size, scale_factor=1.6):
    return int(size * scale_factor)


def span_css(span):
    """Make font flags human readable."""

    # font: font-style, font-variant, font-weight, font-size, font-family
    flags = span["flags"]
    css = []

    if flags & 2**1:
        css.append("italic")
    if flags & 2**4:
        css.append("bold")
    if flags & 2**0:
        css.append("super")

    css.append(f"{scale_size(span['size'],scale_factor=1)}px")

    font = span["font"]
    if font.startswith("NewCenturySchlbk"):
        font = "New Century Schoolbook"

    if flags & 2**3:
        css.append(f"{font}, monospace")
    elif flags & 2**2:
        css.append(f"{font}, serif")
    else:
        css.append(f"{font}, sans-serif")

    return "font: " + " ".join(css)
