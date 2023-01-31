# CRPT2EPUB

The top-line purpose of this project is to convert Congressional Reports into an ePub format.

## Usage

```{code}
docker build -t crpt2epub . # Build the Docker image

docker run -v ${PWD}/data:/tmp/data --rm -ti crpt2epub python main.py /tmp/data/CRPT-117hrpt507.pdf /tmp/data/test.epub
```

## Gotchas (Until I figure these out)

1. Make sure you export poetry dependencies into a "requirements.txt" using the following script: `poetry export -f requirements.txt --without-hashes --output requirements.txt`

---

## Approach

Based on my understanding, there are six types of reports published by Congress, each with a slightly different structure:

1. House Reports on Legislation 
2. Senate Reports on Legislation
3. House Reports on Other Matters (including investigations) 
4. Senate Reports on Other Matters (including investigations)
5. Senate Executive Reports
6. Conference Reports

Currently, these reports are available on Congress.gov and Govinfo.gov in both PDF and TXT formats.

My ultimate goal for this project is to handle automated conversion of reports into an ePub format given a report number (e.g., H. Rept. 117-664). I will plan to use Docker and/or AWS Lambda, with output storage in AWS S3, but can also plan to work with Josh T to figure out what might work better. 

Initially, though, I'll just try and manage conversion locally.

## Plan of attack

1. First, we are going to try and convert everything into HTML.
2. Then, we are going to clean some of the weirdness in the HTML.
3. Then, we're going to use pandoc to convert the HTML into an ePub.

## Known challenges / mitigation strategies

1. *Edge cases.* Some documents (e.g., the Final Report of the Select Committee to Investigate the January 6th Attack on the United States Capitol) are formatted entirely differently from other reports. I am *hoping* that I can generalize the conversion process to create ePubs for all reports, but I am initially going to target the 99% of reports that follow similar structures.
2. *Tables and graphics*. There are a whole bunch of tables that look terrible when converted directly from the PDF and TXT. I am planning on looking for tables and converting them into graphics that are inserted into the ePub.   
3. *Line breaks*. One of the key goals of the project is to promote readability and keep paragraphs together in the conversion process. I plan to use both PDF and TXT/HTML versions to handle this process. BUT, it it possible that when a word is broken across two PDF pages that keeping the line together won't work. I am hoping to correct for this, but flagging that there may be edge cases...
4. Headers/hidden data. In the print (PDF) versions, there are headers with, e.g., page numbers and hidden data that shows up in the standard conversion process. I plan to strip those out and promote readability.
5. *Fonts*. I don't *think* this will be a problem, but I have had issues with embedding fonts in ePubs before...

## (Currently) Out of scope

1. Links for TOC/footnotes. Although it is *theoretically* possible to include hyperlinks in an ePub to headers/footnotes, the current official documents don't include any hyperlinks. I don't plan to add them. 
2. Joint Publications. On the GPO site, there appears to a class of documents called "Featured Joint Publications." There haven't been any since the 110th Congress, so I'm going to just ignore them.
3. "Pixel perfect" conversion. ePubs don't really handle pixel perfect conversions (because they, e.g., allow for larger/smaller margins on different devices). My goal is to focus on flow/readability for the document, not maintaining pixel parity.