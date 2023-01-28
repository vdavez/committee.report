import click
from creport import CReport

import pdb

@click.command()
@click.argument("infile", type=click.File("rb"))
@click.argument("outfile")  # , type=click.File('wb'))
def convert(infile, outfile):
    """Converts a PDF into an ePub

    Args:
        infile (click.File): path to an input file
        outfile (click.File): path to an output file
    """

    doc = CReport(infile)
    return True


if __name__ == "__main__":
    convert()
