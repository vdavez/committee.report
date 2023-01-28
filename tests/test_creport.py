import pytest
from PIL import Image, ImageChops

from src.creport import CReport

class TestCReport:
    doc = CReport('tests/test_report.pdf')

    def test_load_report(self):
        assert self.doc.doc.page_count == 8

    def test_generate_cover_page(self, tmp_path):
        # Generate a temporary file location
        d = tmp_path
        d.mkdir(exist_ok=True)
        outfile = str(d / 'testfile.png')

        # Generate the cover page thumbnail
        self.doc.generate_cover_page(outfile)
        assert len(list(tmp_path.iterdir())) == 1
        
        # Confirm that the images are the same
        image_one = Image.open('tests/test_report1.png')
        outfile = str(d / 'testfile1.png')  # Have to rename it because mutool adds the page number
        image_two = Image.open(outfile)
        diff = ImageChops.difference(image_one, image_two)
        assert diff.getbbox() == None

    def test_generate_html(self):
        assert self.doc.generate_html()