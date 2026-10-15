# Business Contact Scraper

A Python-based tool for collecting publicly available business email addresses and phone numbers from websites.

It uses Requests and Beautiful Soup for regular web pages, with Selenium as a fallback for dynamically rendered content or unsuccessful requests.

## Features

- Extracts emails and phone numbers from website text, links, and structured data.
- Searches additional pages when contact details are missing.
- Supports static and dynamic website scraping.
- Handles request failures and timeouts without interrupting the entire process.
- Tracks progress, records logs, and exports results to CSV and Excel.

## Getting Started

**Requirements:** Python 3.12+, Firefox, and a stable internet connection.

Clone the repository:

```bash
git clone https://github.com/Abdullxploit/business-contact-scraper.git
cd business-contact-scraper
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, activate it using `.venv\Scripts\activate`.

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Open `input/domain.csv` and add the websites you want to scrape under the `domains` column.

```csv
domains
https://example.com
https://example.org
```

Save the file and run:

```bash
python main.py
```

The scraper processes each website, attempts additional extraction when necessary, and saves the results to the configured output folder.

## Configuration

You can adjust the following settings in `config.py`:

| Setting | Default | Purpose |
|---|---|---|
| `INPUT_FOLDER` | `input` | Input CSV location |
| `OUTPUT_FOLDER` | `output` | Saved results |
| `LOG_FOLDER` | `logs` | Application logs |
| `TIMEOUT` | `20` | Request and browser navigation timeout |
| `HEADER` | Predefined | HTTP request headers |

The default settings work without modification, but folder locations and timeouts can be customized.

## Output

The scraper generates `results.csv` and `results.xlsx` containing extracted contact information. Websites that cannot be fetched are recorded in `failed.csv` when applicable.

## Notes

A stable internet connection is recommended for faster and more consistent results. Performance also depends on website response times, accessibility, and page complexity.

Some websites may restrict automated requests or may not publish contact information. Use the tool responsibly, respect website terms and applicable laws, and verify extracted details before using them.

## License

Licensed under the [MIT License](LICENSE).

Copyright © 2026 Abdullahi Muhammad  Tukur.