import logging
from extractor import extract_emails,extract_phone_no,crawl_pages,extract_email_hrefs,crawl_dynamic_pages
from scraper import feth_page_text,fetch_dynamic_page
from input_loader import load_domains
from output_writer import save_to_csv, save_failed_result ,save_to_excel
from progress import show_progress
from logger import get_logger

logger = logging.getLogger(__name__)
def main():
    get_logger()
    domains = load_domains()
    results = []
    failed_results = []
    total = len(domains)

    print("Starting Business Contact Scraper...")
    print(f"Loaded {total} websites.")
    if total == 0:
        print("No websites to Available to process.")
        return
    print("Scraping website contacts...")
    logger.info("scraping started. total website: %s",
                total)

    for completed, domain in enumerate(domains, start=1):

        website_url = domain["domains"]
        text, hrefs, json_ld_scripts = feth_page_text(website_url)

        if text is None:
            logger.warning(
                "Normal fetching failed for %s. Trying Selenium.",
                website_url
            )
            text, hrefs, json_ld_scripts = fetch_dynamic_page(website_url)
        if text is None:
            logger.error(
                "Both normal and Selenium fetching failed for %s",
                website_url
            )

            failed_results.append({
                "website_url": website_url,
                "emails": ["Failed to fetch website"],
                "phone_numbers": ["Failed to fetch website"]
            })
            show_progress(completed, total)
            continue


        emails = extract_emails(text)
        href_emails = extract_email_hrefs(hrefs)
        for email in href_emails:
            if email not in emails:
                emails.append(email)

        numbers = extract_phone_no(text, hrefs, json_ld_scripts)

        if not emails or not numbers:
            emails,numbers = crawl_pages(website_url, emails, numbers)

        if not emails or not numbers:
            dynamic_text, dynamic_hrefs, json_ld_scripts = fetch_dynamic_page(website_url)
            if dynamic_text is not None:
                if not emails:
                    emails = extract_emails(dynamic_text)
                    href_emails = extract_email_hrefs(dynamic_hrefs)

                    for email in href_emails:
                        if email not in emails:
                            emails.append(email)
                if not numbers:
                    numbers = extract_phone_no(dynamic_text, dynamic_hrefs, json_ld_scripts)

            if not emails or not numbers:
                emails, numbers = crawl_dynamic_pages(website_url, emails, numbers)


        if not emails:
            logger.warning("No email found: %s",
                           website_url)
            emails = ["Email not Found"]

        if not numbers:
            logger.warning("No phone number found: %s",
                           website_url)
            numbers = ["Phone_no not found"]

        results.append(
            {
                "website_url": website_url,
                "emails": emails,
                "phone_numbers": numbers
            }
        )
        show_progress(completed, total)
    print()

    save_to_csv(results)
    save_to_excel(results)

    if failed_results:
        save_failed_result(failed_results)

    logger.info(
        "Scraping finished. Total: %s | Processed: %s | Failed: %s",
        total,
        len(results),
        len(failed_results)
    )




if __name__ == "__main__":
    main()


