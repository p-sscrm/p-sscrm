import scholarly
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from fake_useragent import UserAgent
import random

class GoogleScholarScraper:
    def __init__(self, delay_range=(3, 7)):
        self.delay_range = delay_range
        self.results = []
        
    def setup_browser(self):
        """Setup selenium with rotating user agents"""
        ua = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={ua.random}')
        options.add_argument('--headless')
        return webdriver.Chrome(options=options)
        
    def search_with_scholarly(self, query, year_start=None, year_end=None, max_results=100):
        """Search using scholarly library with year filtering"""
        search_query = scholarly.search_pubs(query)
        results = []
        
        try:
            for i, paper in enumerate(search_query):
                if i >= max_results:
                    break
                    
                paper_dict = {
                    'title': paper.bib.get('title'),
                    'author': paper.bib.get('author'),
                    'year': paper.bib.get('year'),
                    'citations': paper.citedby,
                    'url': paper.bib.get('url')
                }
                
                # Apply year filter if specified
                if year_start and year_end:
                    if paper_dict['year'] and year_start <= int(paper_dict['year']) <= year_end:
                        results.append(paper_dict)
                else:
                    results.append(paper_dict)
                    
                # Add random delay to avoid rate limiting
                time.sleep(random.uniform(*self.delay_range))
                
        except Exception as e:
            print(f"Error during scholarly search: {e}")
            
        return results
    
    def search_with_selenium(self, query, num_pages=5):
        """Search using Selenium for more complex scraping"""
        driver = self.setup_browser()
        results = []
        
        try:
            for page in range(num_pages):
                url = f"https://scholar.google.com/scholar?start={page*10}&q={query}"
                driver.get(url)
                
                # Wait for results to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "gs_ri"))
                )
                
                # Extract paper information
                papers = driver.find_elements(By.CLASS_NAME, "gs_ri")
                for paper in papers:
                    title_elem = paper.find_element(By.CLASS_NAME, "gs_rt")
                    authors_elem = paper.find_element(By.CLASS_NAME, "gs_a")
                    
                    paper_dict = {
                        'title': title_elem.text.replace('[PDF] ', '').replace('[HTML] ', ''),
                        'authors': authors_elem.text.split('-')[0],
                        'venue': authors_elem.text.split('-')[1] if len(authors_elem.text.split('-')) > 1 else '',
                        'url': title_elem.find_element(By.TAG_NAME, "a").get_attribute("href") if title_elem.find_elements(By.TAG_NAME, "a") else None
                    }
                    
                    results.append(paper_dict)
                
                time.sleep(random.uniform(*self.delay_range))
                
        except Exception as e:
            print(f"Error during selenium search: {e}")
        finally:
            driver.quit()
            
        return results
    
    def export_results(self, results, filename='scholar_results.csv'):
        """Export results to CSV file"""
        df = pd.DataFrame(results)
        df.to_csv(filename, index=False)
        return filename

def main():
    scraper = GoogleScholarScraper()
    
    # Example usage with scholarly
    scholarly_results = scraper.search_with_scholarly(
        query="software engineering systematic literature review",
        year_start=2020,
        year_end=2024,
        max_results=50
    )
    
    # Example usage with selenium
    selenium_results = scraper.search_with_selenium(
        query="software engineering systematic literature review",
        num_pages=3
    )
    
    # Export results
    scraper.export_results(scholarly_results, 'scholarly_results.csv')
    scraper.export_results(selenium_results, 'selenium_results.csv')

if __name__ == "__main__":
    main()
