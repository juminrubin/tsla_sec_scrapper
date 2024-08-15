# Project: SEC Proxy Vote Scraper

import os
import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
import json
import logging
from datetime import datetime

# Configuration
CONFIG = {
    'BASE_URL': "https://www.sec.gov/Archives/edgar/data/",
    'OUTPUT_DIR': "sec_proxy_data",
    'MAX_RETRIES': 3,
    'SLEEP_MIN': 1,
    'SLEEP_MAX': 5
}

# Setup logging
logging.basicConfig(filename='sec_scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ProxyVoteScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {'User-Agent': self.ua.random}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        if not os.path.exists(CONFIG['OUTPUT_DIR']):
            os.makedirs(CONFIG['OUTPUT_DIR'])

    def _get_soup(self, url, retries=0):
        """Fetch the HTML content with retry logic."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            if retries < CONFIG['MAX_RETRIES']:
                logging.warning(f"Request failed, retrying. Error: {e}")
                time.sleep(random.uniform(CONFIG['SLEEP_MIN'], CONFIG['SLEEP_MAX']))
                return self._get_soup(url, retries + 1)
            else:
                logging.error(f"Failed to fetch {url} after {retries} retries.")
                return None

    def find_proxy_votes(self, cik):
        """Find proxy votes for a company by CIK."""
        url = f"{CONFIG['BASE_URL']}{cik}/"
        soup = self._get_soup(url)
        if not soup:
            return []

        # Look for proxy statements in the list of filings
        proxy_links = soup.find_all("a", href=lambda href: href and "proxy" in href.lower())
        return [f"{url}{link['href']}" for link in proxy_links]

    def scrape_vote_results(self, url):
        """Scrape the vote results from a proxy statement."""
        soup = self._get_soup(url)
        if not soup:
            return {}

        # Here we'd need to parse the actual content, which might be in various formats
        # For simplicity, let's assume we're looking for a table or list of vote results
        results = soup.find_all("tr", class_="vote-result")  # This class is fictional for this example
        return {result.find("td").text: result.find_all("td")[1].text for result in results}

    def save_results(self, cik, results):
        """Save scraped results to JSON file."""
        filename = f"{CONFIG['OUTPUT_DIR']}/{cik}_proxy_votes.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        logging.info(f"Results saved to {filename}")

    def run(self, cik):
        """Main scraping function."""
        proxy_urls = self.find_proxy_votes(cik)
        results = {}

        for url in proxy_urls:
            time.sleep(random.uniform(CONFIG['SLEEP_MIN'], CONFIG['SLEEP_MAX']))
            vote_results = self.scrape_vote_results(url)
            if vote_results:
                results[url] = vote_results
                logging.info(f"Scraped data from {url}")
            else:
                logging.warning(f"No data found at {url}")

        if results:
            self.save_results(cik, results)
        else:
            logging.info("No proxy vote data found for this CIK.")

if __name__ == "__main__":
    # Example usage
    scraper = ProxyVoteScraper()
    cik = "0001318605"  # Example CIK for Tesla Inc.
    scraper.run(cik)
    print("Scraping complete. Check the log for details.")