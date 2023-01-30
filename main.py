import click
from src.creport import CReport
import tempfile
import subprocess
import os

@click.command()
@click.argument("infile", type=click.File("rb"))
@click.argument("outfile", type=click.File("w"))
def convert(infile, outfile):
    """Converts a PDF into an ePub

    Args:
        infile (click.File): path to an input file
        outfile (click.File): path to an output file
    """

    if "hrpt" in infile.name:
        author = "U.S. House of Representatives"
    else:
        author = "U.S. Senate"
    doc = CReport(infile)
    fp = tempfile.NamedTemporaryFile(mode="w", delete=False)
    fp.write(doc.html)
    fp.close()

    cfp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    doc.generate_cover_page(outfile=cfp.name)
    cfp.close()

    title = os.path.basename(infile.name)

    cover_image = cfp.name.replace(".png", "1.png")
    subprocess.check_call([
        "pandoc",
        fp.name,
        "-M",
        f"title={title.replace('.pdf','')}",
        "-M",
        f"author={author}",
        "--epub-cover-image",
        cover_image,
        "--epub-embed-font",
        "src/ncsr55w.ttf",
        "-M",
        "epub-title-page=false",
        "-f",
        "html",
        "-t", 
        "epub3",
        "-o",
        outfile.name
        ])

    return True


if __name__ == "__main__":
    convert()
