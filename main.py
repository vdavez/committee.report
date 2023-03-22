#!/usr/bin/env python3
import click
from src.creport import CReport
import tempfile
import subprocess
import os
import boto3
import requests
import datetime
import sys, logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.info("Starting...")
s3 = boto3.client("s3")
DATA_DOT_GOV_API_KEY = os.environ.get("DATA_DOT_GOV_API_KEY")

yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

@click.group()
def cli():
    pass


@click.command()
@click.argument("day", default=yesterday)
def getfromday(day):
    govinfo_url = f"https://api.govinfo.gov/published/{day}?pageSize=100&collection=CRPT&offsetMark=%2A&api_key={DATA_DOT_GOV_API_KEY}"
    response = requests.get(govinfo_url).json()
    if response["count"] == 0:
        return 0
    for r in response["packages"]:
        logging.info(f"Converting {r['packageId']}")
        convert(r["packageId"])


@click.command()
@click.argument("report_number")
def report(report_number):
    logging.info(f"Converting {report_number}")
    convert(report_number)


cli.add_command(getfromday)
cli.add_command(report)


def convert(report_number):
    """Converts a PDF into an ePub

    Args:
        report_number: (e.g., CRPT-117hrpt507)
    """

    if "hrpt" in report_number:
        author = "U.S. House of Representatives"
    else:
        author = "U.S. Senate"

    # Get the file from S3
    s3_infile_path = f"pdfs/{report_number}.pdf"
    local_infile_path = f"{report_number}.pdf"
    local_outfile_path = f"{report_number}.epub"
    s3_outfile_path = f"epubs/{report_number}.epub"

    # Download and access the file from S3
    govinfo_link = (
        f"https://www.govinfo.gov/content/pkg/{report_number}/pdf/{report_number}.pdf"
    )
    logging.info(f"Downloading the PDF from {govinfo_link}")
    response = requests.get(govinfo_link)
    with open(local_infile_path, "wb") as f:
        f.write(response.content)
        doc = CReport(local_infile_path)

    fp = tempfile.NamedTemporaryFile(mode="w", delete=False)
    fp.write(doc.html)
    fp.close()

    cfp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    doc.generate_cover_page(outfile=cfp.name)
    cfp.close()

    cover_image = cfp.name.replace(".png", "1.png")

    logging.info("Generating the ePub")
    subprocess.check_call(
        [
            "pandoc",
            fp.name,
            "-M",
            f"title={report_number}",
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
            local_outfile_path,
        ]
    )

    with open(local_outfile_path, "rb") as f:
        logging.info(f"Uploading to s3 @ s3://crpts/{s3_outfile_path}")
        s3.upload_fileobj(f, "crpts", s3_outfile_path)

    return True


if __name__ == "__main__":
    cli()
