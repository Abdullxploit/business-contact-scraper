import csv
from pathlib import Path
from openpyxl import Workbook
from config import OUTPUT_FOLDER
import logging

logger = logging.getLogger(__name__)
def save_to_csv(results):
    try:
        output_path = Path(OUTPUT_FOLDER)/"results.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(["website_url", "emails", "phone_numbers"])

            for result in results:
                writer.writerow([
                    result["website_url"],
                    ", ".join(result["emails"]),
                    ", ".join(result["phone_numbers"])
                ])
        logger.info("CSV saved successfully at: %s",
                    output_path)

    except OSError as error:
        logger.error("Failed to save CSV: %s",
                     error)
        raise

def save_to_excel(results):
    try:
        output_path = Path(OUTPUT_FOLDER) / "results.xlsx"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Business Contacts"

        sheet.append(["website_url", "emails", "phone_numbers"])

        for result in results:
            sheet.append([
                result["website_url"],
                ", ".join(result["emails"]),
                ", ".join(result["phone_numbers"])
            ])

        for column in sheet.columns:
            max_length = 0

            for cell in column:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))

            column_letter = column[0].column_letter
            sheet.column_dimensions[column_letter].width = max_length + 2

        workbook.save(output_path)

        logger.info("Excel saved successfully at: %s",
                    output_path)

    except OSError as error:
        logger.error("Failed to save Excel: %s",
              error)
        raise

def save_failed_result(failed_result):
    try:
        output_path = Path(OUTPUT_FOLDER)/"failed.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["website_url", "emails", "phone_numbers"])

            for result in failed_result:
                writer.writerow([
                    result["website_url"],
                    ", ".join(result["emails"]),
                    ", ".join(result["phone_numbers"])
                ])

        logger.info("failed website CSV saved successfully at: %s",
                    output_path)

    except OSError as error:
        logger.error("Failed to save failed website to CSV: %s",
                     error)
        raise
