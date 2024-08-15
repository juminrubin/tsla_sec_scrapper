import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


class SECScraper:
    BASE_URL = "https://www.sec.gov"
    SEARCH_URL = f"{BASE_URL}/cgi-bin/browse-edgar"

    def __init__(self, cik, filing_type="10-K"):
        self.cik = cik
        self.filing_type = filing_type
        self.session = requests.Session()
        self.filings = []

    def fetch_filings(self, start=0, count=40):
        """Fetch filings for the initialized CIK and filing type."""
        params = {
            'action': 'getcompany',
            'CIK': self.cik,
            'type': self.filing_type,
            'start': start,
            'count': count,
            'output': 'atom',
        }

        response = self.session.get(self.SEARCH_URL, params=params)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            return None

    def parse_filings(self, xml_data):
        """Parse XML data returned from the SEC EDGAR."""
        soup = BeautifulSoup(xml_data, "lxml")
        entries = soup.find_all('entry')

        for entry in entries:
            filing = self.extract_filing_details(entry)
            self.filings.append(filing)

    def extract_filing_details(self, entry):
        """Extract relevant details from a single SEC filing entry."""
        filing = {
            "title": entry.find("title").text,
            "link": entry.find("link")["href"],
            "summary": entry.find("summary").text if entry.find("summary") else "N/A",
            "filing_date": entry.find("updated").text,
        }
        return filing

    def save_to_csv(self, filename):
        """Save the scraped data to a CSV file."""
        df = pd.DataFrame(self.filings)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def run(self, max_filings=100, batch_size=40):
        """Run the scraper to collect filings and save them to a CSV file."""
        for start in range(0, max_filings, batch_size):
            xml_data = self.fetch_filings(start=start, count=batch_size)
            if xml_data:
                self.parse_filings(xml_data)
            time.sleep(1)  # Be considerate of SEC servers

        self.save_to_csv(f"{self.cik}_{self.filing_type}.csv")


if __name__ == "__main__":
    cik = input("Enter CIK of the company: ")
    filing_type = input("Enter the filing type (e.g., 10-K, 10-Q): ")

    scraper = SECScraper(cik, filing_type)
    scraper.run()
