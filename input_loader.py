import csv
import os
from config import INPUT_FOLDER

def load_domains():
    path = os.path.join(INPUT_FOLDER, "domains.csv")
    domains = []

    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            domains.append(row)

    return domains

load_domains()