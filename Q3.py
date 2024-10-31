import csv
from collections import Counter

# Define the list to store license names
licenses = []

# Read the CSV file with UTF-8 encoding
with open('repositories.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:

        license_name = row.get('license_name', '').strip()
        if license_name:
            licenses.append(license_name)

license_counts = Counter(licenses)

top_3_licenses = [license for license, count in license_counts.most_common(3)]

for el in top_3_licenses:
    print(el, end=',')
