from src.helpers import span_css

def test_span_css():
    span = {'size': 7.0, 'flags': 4, 'font': 'NewCenturySchlbk-Roman', 'color': 0, 'ascender': 0.9800000190734863, 'descender': -0.2150000035762787, 'text': '29–008 ', 'origin': (163.0, 691.0), 'bbox': (163.0, 684.1400146484375, 188.29798889160156, 692.5050048828125)}
    assert span_css(span) == "font: 11px NewCenturySchlbk-Roman, serif"