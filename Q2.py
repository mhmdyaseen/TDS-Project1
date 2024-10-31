import csv
from datetime import datetime

users_in_barcelona = []

with open('users.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        location = row['location'].strip().lower()

        if 'barcelona' in location:
            users_in_barcelona.append({
                'login': row['login'],
                'created_at': datetime.strptime(row['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            })

sorted_users = sorted(users_in_delhi, key=lambda x: x['created_at'])

top_5_earliest_logins = [user['login'] for user in sorted_users[:5]]

for el in top_5_earliest_logins:
  print(el, end=',')
