from bs4 import BeautifulSoup
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from requests import RequestException
from selenium.common.exceptions import WebDriverException, TimeoutException
from config import HEADER,TIMEOUT
import logging


logger = logging.getLogger(__name__)
def feth_page_text(url):
    try:
        response = requests.get(url, timeout=TIMEOUT, headers=HEADER)
        response.raise_for_status()

        content = (response.content)
        soup = BeautifulSoup(content, "html.parser")
        html_text = soup.get_text(" ", strip=True)

        links = soup.find_all("a", href=True)
        hrefs = []
        for link in links:
           link = link["href"]
           hrefs.append(link)

        json_ld_scripts = soup.find_all("script",
                                        type="application/ld+json")

        return html_text,hrefs, json_ld_scripts

    except RequestException as error:
        logger.warning(
            "Failed to fetch page %s: %s",
            url,
            error
        )
        return None, [], []

def fetch_dynamic_page(url):
    browser = None

    try:
        firefox_options = Options()
        firefox_options.add_argument("--headless")

        browser = webdriver.Firefox(options=firefox_options)
        browser.set_page_load_timeout(TIMEOUT)

        browser.get(url)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")
        html_text = soup.get_text(" ", strip=True)

        links = soup.find_all("a", href=True)
        hrefs = []

        for link in links:
            href = link["href"]
            hrefs.append(href)

        json_ld_scripts = soup.find_all(
            "script",
            type="application/ld+json"
        )

        return html_text, hrefs, json_ld_scripts

    except (WebDriverException, TimeoutException) as error:
        logger.warning(
            "Failed to fetch dynamic page %s: %s",
            url,
            error
        )
        return None, [], []

    finally:
        if browser is not None:
            browser.quit()


