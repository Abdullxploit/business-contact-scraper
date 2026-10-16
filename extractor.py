import re
import requests
import json
from bs4 import BeautifulSoup
import phonenumbers
from urllib.parse import urljoin
from scraper import feth_page_text,fetch_dynamic_page
import logging

email_pattern = r"[\w.-]+@[\w.-]+\.[A-Za-z]{2,}"
phone_no_pattern = r"\+?\d+(?: |-)?\(?\d+\)?(?:(?: |-)\d+)?(?:(?: |-)\d+)?"

contact_pages = [
    "contact",
    "contact-us",
    "about",
    "about-us",
    "team"
]


logger = logging.getLogger(__name__)
def extract_emails(text):
    emails = re.findall(email_pattern, text)
    uniques_emails = []

    for email in emails:
        if email not in uniques_emails:
            uniques_emails.append(email)
            
    return uniques_emails

def find_json_ld_telephone(data, numbers):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "telephone" and isinstance(value, str):
                numbers.append(value)

            find_json_ld_telephone(value, numbers)

    if isinstance(data, list):
        for item in data:
            find_json_ld_telephone(item, numbers)

    return numbers

def extract_json_ld_phone(json_ld_script):
    numbers = []

    for script in json_ld_script:
        try:
            data = json.loads(script.string)
        except(json.JSONDecodeError, TypeError) as error:
            logger.debug("Skipping invalid JSON-LD script: %s",
                         error)
            continue
        find_json_ld_telephone(data, numbers)

    return numbers

def clean_phone_numbers(numbers):
    cleaned_numbers= []

    for number in numbers:
        number = number.removeprefix("tel:").strip()

        try:
            parsed = phonenumbers.parse(number, "NG")

            if phonenumbers.is_valid_number(parsed):
                formatted = phonenumbers.format_number(
                    parsed,
                    phonenumbers.PhoneNumberFormat.E164
                )

                if formatted not in cleaned_numbers:
                    cleaned_numbers.append(formatted)

        except phonenumbers.NumberParseException as error:
            logger.debug(
                "Skipping unparseable phone number %s: %s",
                number,
                error
            )
            continue

    return cleaned_numbers

def extract_phone_no(text,hrefs, json_ld_script):
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", "", text)
    phone_no = re.findall(phone_no_pattern, text)
    uniques_numbers = []

    for link in hrefs:
        if link.startswith("tel"):
            number = link.removeprefix("tel:")
            digits = re.sub(r"\D", "", number)

            if len(digits) >= 9 and len(digits) <= 15:
                if number not in uniques_numbers:
                    uniques_numbers.append(number)


    for number in phone_no:
        digits = re.sub(r"\D", "", number)

        if len(digits) >= 9 and len(digits) <= 15:
            if number not in uniques_numbers:
                uniques_numbers.append(number)

    json_ld_numbers = extract_json_ld_phone(json_ld_script)
    for number in json_ld_numbers:
        if number not in uniques_numbers:
            uniques_numbers.append(number)

    return clean_phone_numbers(uniques_numbers)

def decode_cf_email(encoded):
    key = int(encoded[:2], 16)
    email = ""

    for i in range(2, len(encoded), 2):
        number = int(encoded[i:i+2], 16)
        email += chr(number ^ key)

    return email

def extract_email_hrefs(hrefs):
    href_emails = []

    for href in hrefs:
        if "/cdn-cgi/l/email-protection#" in href:
            encoded = href.split("#")[1]
            try:
                decoded_email = decode_cf_email(encoded)
                href_emails.append(decoded_email)
            except (ValueError, IndexError) as error:
                logger.warning(
                    "Failed to decode protected email from %s: %s",
                    href,
                    error
                )
                continue
        else:
            found_emails = extract_emails(href)
            href_emails.extend(found_emails)

    return href_emails


def crawl_pages(url, emails, phone_no):
    for page in contact_pages:
        page_url = urljoin(url, "/" + page)
        text, hrefs, json_ld_scripts = feth_page_text(page_url)
        if text is None:
            continue

        if not emails:
            emails = extract_emails(text)
            href_emails = extract_email_hrefs(hrefs)
            for email in href_emails:
                if email not in emails:
                    emails.append(email)

        if not phone_no:
            phone_no = extract_phone_no(text, hrefs, json_ld_scripts)

        if  emails and phone_no:
            logger.info(
                "Contact details found while crawling %s",
                page_url)
            break
    return emails,phone_no

def crawl_dynamic_pages(url, emails, phone_no):
    for page in contact_pages:
        page_url = urljoin(url, "/" + page)

        text, hrefs, json_ld_scripts = fetch_dynamic_page(page_url)
        if text  is None:
            continue
        if not emails:
            emails = extract_emails(text)
            href_emails = extract_email_hrefs(hrefs)
            for email in href_emails:
                if email not in emails:
                    emails.append(email)

        if not phone_no:
            phone_no = extract_phone_no(text, hrefs, json_ld_scripts)

        if emails and phone_no:
            logger.info(
                "Contact details found through dynamic crawling: %s",
                page_url
            )
            break

    return emails, phone_no