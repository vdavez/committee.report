FROM --platform=linux/amd64 python:3.11-slim-bullseye AS compile-image
RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM --platform=linux/amd64 python:3.11-slim-bullseye AS build-image
RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN apt-get install -y mupdf mupdf-tools pandoc
COPY --from=compile-image /opt/venv /opt/venv

# Create non-root user
RUN useradd --create-home appuser -u 1000
USER appuser
WORKDIR /home/appuser

COPY src/ src/
COPY main.py .

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
CMD ["python", "main.py"]