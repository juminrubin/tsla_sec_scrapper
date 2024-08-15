# SEC Scraper

This project is a Python-based scraper for retrieving financial filings from the SEC EDGAR database. It uses the `requests` and `BeautifulSoup` libraries to fetch and parse data, and `pandas` to save the data into a CSV file.

## Features

- Scrapes SEC filings such as 10-K and 10-Q forms.
- Saves the scraped data into a CSV file.
- Modular, class-based design for easy extension and maintenance.

## Requirements

- Python 3.x
- Required Python packages (install using `requirements.txt`):
  - `requests`
  - `beautifulsoup4`
  - `pandas`

## Installation

1. Clone this repository.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt

## Usage

````bash
python sec_scraper.py
