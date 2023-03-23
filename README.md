# committee.report

The top-line purpose of this project is to convert Congressional Committee Reports into an ePub format.

You can now download new committee reports predicting a URL! For example:

https://committee.report/118hrpt1

## How it works

The project uses a handful of different tools to automate the conversion of the reports.

- Uses the [GovInfo API](https://api.govinfo.gov/docs/) and GovInfo predictable URL structure to find the relevant PDFs for a given committee report.
- Uses [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) (and the underlying tool MuPDF) to extract the text from the PDF and to create a screenshot of the front page. This is where most of the work in conversion exists and it mainly works by creating a light HTML version of the document.
- Uses [Pandoc](https://pandoc.org/MANUAL.html) to convert the generated HTML into an ePub.
- Uses [Amazon S3](https://docs.aws.amazon.com/s3/index.html) and [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html) to store the ePub.
- Uses [Docker](docker.com) to create a container for the code and we deploy the container image to [Amazon ECR](https://docs.aws.amazon.com/ecr/index.html) for hosting.
- Uses [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/index.html) to create a cron job that, every day, calls [AWS ECS](https://docs.aws.amazon.com/ecs/) to run a task.
- We provision the AWS infrastructure using [Terraform](https://developer.hashicorp.com/terraform).

## Using it locally

To use the tool locally, you need to have docker installed and then build the image.

```{code}
./build.sh # Build the Docker image
```

To convert a single report, get the report number (with the structure like `CRPT-118hrpt3`), and run the following command. [Note, I have it hardcoded to deploy to a single S3 bucket, but this could be changed...]

```{code}
docker run crpt2epub python main.py report <report_number>
```

To get (up to) the 100 most-recent reports from GovInfo, run the following command. [Note, I exploit this to set the date as today's date and this allows the script to automatically pull and convert the most recent reports...]

```{code}
docker run crpt2epub python main.py getfromday <date>
```

## Some gotchas for developers

1. If you're planning on doing local development and/or change the python dependencies, you'll need to have [poetry](https://python-poetry.org/) installed. If you do make changes, you need to export poetry dependencies into a "requirements.txt" using the following script: `poetry export -f requirements.txt --without-hashes --output requirements.txt`.


## Background

Based on my understanding, there are six types of reports published by Congress, each with a slightly different structure:

1. House Reports on Legislation
2. Senate Reports on Legislation
3. House Reports on Other Matters (including investigations)
4. Senate Reports on Other Matters (including investigations)
5. Senate Executive Reports
6. Conference Reports

Currently, these reports are available on Congress.gov and Govinfo.gov in both PDF and TXT formats.

My goal for this project was to handle automated conversion of reports into an ePub format given a report number (e.g., H. Rept. 117-664).

## Known challenges / mitigation strategies

1. *Edge cases.* Some documents (e.g., the Final Report of the Select Committee to Investigate the January 6th Attack on the United States Capitol) are formatted entirely differently from other reports. I *hope* that the conversion process is good enough for ePubs for all reports, but I haven't tested all of them.
2. *Line breaks*. One of the key goals of the project is to promote readability and keep paragraphs together in the conversion process. When a word is broken across two PDF pages, however, keeping the line together doesn't work. I had hoped to correct for this, but it's very hard indeed...

## Future improvements

1. Links for TOC/footnotes. Although it is *theoretically* possible to include hyperlinks in an ePub to headers/footnotes, the current official documents don't include any hyperlinks.
2. Joint Publications. On the GPO site, there appears to a class of documents called "Featured Joint Publications." There haven't been any since the 110th Congress, so I just ignored them.
