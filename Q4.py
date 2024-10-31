import csv
from collections import Counter

companies = []

with open('users.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Get and clean up the company field (ignore empty values)
        company = row.get('company', '').strip()
        if company:
            companies.append(company)

company_counts = Counter(companies)

most_common_company = company_counts.most_common(1)

try:
    print(most_common_company[0][0])
except:
    print("No company data found.")
