from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import time

# ========== CONFIGURATION ==========
URL = 'https://polymarket.com/elections'
DISTRICT_LINKS = [
    'https://polymarket.com/event/congressional-district-1st-maine-presidential-election-winner',
    'https://polymarket.com/event/congressional-district-2nd-maine-presidential-election-winner',
    'https://polymarket.com/event/congressional-district-1st-nebraska-presidential-election-winner',
    'https://polymarket.com/event/congressional-district-2nd-nebraska-presidential-election-winner',
    'https://polymarket.com/event/congressional-district-3rd-nebraska-presidential-election-winner',
]
OUTPUT_TIME = time.strftime("%Y-%m-%d_%H-%M", time.localtime())
OUTPUT_FILE = f'polymarket_elections_{OUTPUT_TIME}.csv'

# ========== SELENIUM OPTIONS ==========
def get_chrome_options():
    options = Options()
    options.add_argument("--window-position=-2400,-2400") # Move window off-screen
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--disable-proxy-certificate-handler')
    return options

# ========== SCRAPING HELPERS ==========
def get_page_source(url, driver):
    driver.get(url)
    sleep(1)
    return driver.page_source

def extract_votes(soup, driver):
    """
    Extracts republican and democratic votes from the current soup.
    If the democratic votes are hidden, clicks the button to reveal them.
    Returns: (republican_vote, democratic_vote)
    """
    try:
        rep_vote = soup.find('div', class_='c-gBrBnR c-kJKHmO c-gBrBnR-ifgGdkS-css').get_text().split(' ')[-1][:-3].replace('¢', '') + '%'
        try:
            dem_vote = soup.find('div', class_='c-gBrBnR c-kJKHmO c-gBrBnR-ibMWmgq-css').get_text().split(' ')[-1][:-3].replace('¢', '') + '%'
        except:
            # Reveal hidden data
            driver.find_element(By.CSS_SELECTOR, 'button.c-gBrBnR.c-jWXdIq').click()
            sleep(0.5)
            source2 = driver.page_source
            soup2 = BeautifulSoup(source2, 'html.parser')
            dem_vote = soup2.find('div', class_='c-gBrBnR c-kJKHmO c-gBrBnR-ibMWmgq-css').get_text().split(' ')[-1][:-3].replace('¢', '') + '%'
        return rep_vote, dem_vote
    except Exception as e:
        print(f"Error extracting votes: {e}")
        return None, None

def extract_title_from_link(link):
    """Extracts and formats the title from a link."""
    return link.split('/')[2].replace('-', ' ').title().split('Presidential')[0][:-1]

def extract_title_from_district(link):
    """Extracts and formats the title for district links."""
    tt = link.split('/')[-1].replace('-', ' ').title().split('Presidential')[0][:-1]
    if len(tt) > 24:
        leter_lower = tt[24].lower()
        return tt[:24] + leter_lower + tt[25:]
    return tt

# ========== MAIN SCRAPING LOGIC ==========
def scrape_map_states(driver, url):
    """Scrapes all states from the main map."""
    titles, rep_votes, dem_votes = [], [], []
    source = get_page_source(url, driver)
    soup = BeautifulSoup(source, 'lxml')
    g_element = soup.find(id='map-svg-group')
    a_elements = g_element.find_all('a')
    for link in a_elements:
        state_url = 'https://polymarket.com' + link['href']
        state_source = get_page_source(state_url, driver)
        state_soup = BeautifulSoup(state_source, 'html.parser')
        title = extract_title_from_link(link['href'])
        butt = state_soup.find('button', class_='c-PJLV c-cRTVfI')
        if butt.find('p', class_='c-cZBbTr').get_text() == 'Republican':
            rep, dem = extract_votes(state_soup, driver)
        else:
            dem, rep = extract_votes(state_soup, driver)
        titles.append(title)
        rep_votes.append(rep)
        dem_votes.append(dem)
        print(f'Title: {title}, Republican Votes: {rep}, Democratic Votes: {dem}')
    return titles, rep_votes, dem_votes

def scrape_districts(driver, links):
    """Scrapes all specified congressional districts."""
    titles, rep_votes, dem_votes = [], [], []
    for link in links:
        district_source = get_page_source(link, driver)
        district_soup = BeautifulSoup(district_source, 'html.parser')
        title = extract_title_from_district(link)
        butt = district_soup.find('button', class_='c-PJLV c-cRTVfI')
        if butt.find('p', class_='c-cZBbTr').get_text() == 'Republican':
            rep, dem = extract_votes(district_soup, driver)
        else:
            dem, rep = extract_votes(district_soup, driver)
        titles.append(title)
        rep_votes.append(rep)
        dem_votes.append(dem)
        print(f'Title: {title}, Republican Votes: {rep}, Democratic Votes: {dem}')
    return titles, rep_votes, dem_votes

# ========== MAIN EXECUTION ==========
def main():
    chrome_options = get_chrome_options()
    driver = webdriver.Chrome(options=chrome_options)

    # Scrape map states
    titles1, rep_votes1, dem_votes1 = scrape_map_states(driver, URL)
    # Scrape districts
    titles2, rep_votes2, dem_votes2 = scrape_districts(driver, DISTRICT_LINKS)

    # Combine results
    all_titles = titles1 + titles2
    all_rep_votes = rep_votes1 + rep_votes2
    all_dem_votes = dem_votes1 + dem_votes2

    # Save to CSV
    df = pd.DataFrame({
        'Title': all_titles,
        'Republican Votes': all_rep_votes,
        'Democratic Votes': all_dem_votes
    })
    df.to_csv(OUTPUT_FILE, sep=',', index=False)
    print(f"Saved results to {OUTPUT_FILE}")

    driver.quit()

if __name__ == "__main__":
    main()