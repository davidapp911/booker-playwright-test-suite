FROM mcr.microsoft.com/playwright/python:v1.60.0-noble
WORKDIR /app
COPY pyproject.toml .
RUN pip install .
RUN playwright install
COPY . .
CMD ["pytest"]