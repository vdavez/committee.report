from src.helpers import span_css, handle_indent
import json

def test_span_css():
    span = {'size': 7.0, 'flags': 4, 'font': 'NewCenturySchlbk-Roman', 'color': 0, 'ascender': 0.9800000190734863, 'descender': -0.2150000035762787, 'text': '29–008 ', 'origin': (163.0, 691.0), 'bbox': (163.0, 684.1400146484375, 188.29798889160156, 692.5050048828125)}
    assert span_css(span) == "font: 11px New Century Schoolbook, serif"


def test_handle_indent():
    with open("tests/test_blocks.json","r") as jsonfile:
        test_blocks = json.load(jsonfile)
    
    first_span = test_blocks[0][9]["lines"][0]["spans"][0]

    first_paragraph = """The resolution provides for consideration of H.R. 3843, the Merger Filing Fee Modernization Act of 2022, under a closed rule. The """

    assert handle_indent(test_blocks[0][9], 0, 0, first_span) == "<br>&nbsp;&nbsp;" + first_paragraph