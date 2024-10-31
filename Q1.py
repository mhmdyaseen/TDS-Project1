# Q1:
import csv

users_in_barcelona = []

with open('users.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        location = row['location'].strip().lower()

        if 'barcelona' in location:
            users_in_barcelona.append({
                'login': row['login'],
                'followers': int(row['followers'])
            })

top_users = sorted(users_in_barcelona, key=lambda x: x['followers'], reverse=True)

top_5_logins = [user['login'] for user in top_users[:5]]

for el in top_5_logins:
  print(el, end=',')
