def add_indent(b0, span, char=5):
    """Check to see if a span's bbox is greater than the block's bbox. If it is, add an indent"""
    
    # TODO: 
    # 
    # 1. Fix the extra <br>

    b1 = span["bbox"][0]
    if b1 == b0:
        chars = ""
    elif b1 > b0:
        chars = "<br>" + int((b1 - b0) / char)*" "
    elif span["text"][0] == "(":
        chars = "<br>" + chars
    elif span["text"][0] == "—":
        chars = "<br>" + chars
    text = chars + span["text"]
    return text

def add_redaction(page, span):
    """Check if white text, add redaction"""
    if span['color']==16777215:
        annot = page.add_redact_annot(fitz.Rect(span['bbox']), fill=True)
    return True


def scale_size(size, scale_factor=1.6):
    return int(size * scale_factor)

def span_css(span):
    """Make font flags human readable."""

    # font: font-style, font-variant, font-weight, font-size, font-family 
    flags = span["flags"]
    css = []

    if flags & 2 ** 1:
        css.append("italic")
    if flags & 2 ** 4:
        css.append("bold")
    if flags & 2 ** 0:
        css.append("super")

    css.append(f"{scale_size(span['size'])}px")


    if flags & 2 ** 3:
        css.append(f"{span['font']}, monospace")
    elif flags & 2 ** 2:
        css.append(f"{span['font']}, serif")
    else:
        css.append(f"{span['font']}, sans-serif")
    
    return "font: " + " ".join(css)
