import pandas as pd
from bs4 import BeautifulSoup

def extract_filing_details(entry):
    """Extract relevant details from a single SEC filing entry."""
    filing = {
        "title": entry.find("title").text,
        "link": entry.find("link")["href"],
        "summary": entry.find("summary").text if entry.find("summary") else "N/A",
        "filing_date": entry.find("updated").text,
    }
    return filing

def save_to_csv(data, filename):
    """Save the scraped data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
