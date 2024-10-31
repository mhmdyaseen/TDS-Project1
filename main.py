import requests
import csv
import os
import time
from dotenv import load_dotenv

load_dotenv()

token =  #Your GitHub API Token
headers = {'Authorization': f'token {token}'}

def save_users_to_csv(filename='users.csv'): # Function to save user data to CSV
    fieldnames = ['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at']
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        page = 1
      
        while True:
            url = f'https://api.github.com/search/users?q=location:Barcelona+followers:>100&per_page=30&page={page}'
            response = requests.get(url, headers=headers)
            users_data = response.json()

            if 'items' not in users_data or not users_data['items']:
                break
            
            for user in users_data['items']:
                user_url = f"https://api.github.com/users/{user['login']}"
                user_info = requests.get(user_url, headers=headers).json()

                writer.writerow({
                    'login': user_info.get('login'),
                    'name': user_info.get('name'),
                    'company': user_info.get('company', '').strip().lstrip('@').upper(),
                    'location': user_info.get('location'),
                    'email': user_info.get('email'),
                    'hireable': user_info.get('hireable'),
                    'bio': user_info.get('bio'),
                    'public_repos': user_info.get('public_repos'),
                    'followers': user_info.get('followers'),
                    'following': user_info.get('following'),
                    'created_at': user_info.get('created_at')
                })
              
            page += 1
    print(f"User data saved to users.csv")

def fetch_repositories(user_login): # Function to fetch repositories for a user
    repos_data = []
    page = 1
  
    while True:
        repos_url = f"https://api.github.com/users/{user_login}/repos"
        response = requests.get(repos_url, headers=headers, params={'per_page': 100, 'page': page})
        repos = response.json()
        
        if not repos or 'message' in repos:
            break
        repos_data.extend(repos)
        
        if len(repos) < 100:
            break
        page += 1
        time.sleep(1)  # Delay to avoid rate limiting
      
    return repos_data

def save_repositories_to_csv(user_file='users.csv', repo_file='repositories.csv'): # Function to save repository data to CSV
    with open(user_file, 'r', encoding='utf-8') as userfile:
        users = list(csv.DictReader(userfile))

    with open(repo_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        start_time = time.time()
        
        for index, user in enumerate(users, start=1):
            user_login = user.get('login')
            if not user_login:
                print(f"Warning: 'login' key not found in user data: {user}")
                continue
            
            repositories = fetch_repositories(user_login)
            for repo in repositories:
                writer.writerow({
                    'login': user_login,
                    'full_name': repo.get('full_name'),
                    'created_at': repo.get('created_at'),
                    'stargazers_count': repo.get('stargazers_count'),
                    'watchers_count': repo.get('watchers_count'),
                    'language': repo.get('language'),
                    'has_projects': repo.get('has_projects'),
                    'has_wiki': repo.get('has_wiki'),
                    'license_name': repo.get('license', {}).get('key')
                })
                
            elapsed_time = time.time() - start_time
            estimated_total_time = (elapsed_time / index) * len(users)
            remaining_time = estimated_total_time - elapsed_time
            print(f"Estimated time remaining: {remaining_time:.2f} seconds")

    print(f"Repository data saved to repositories.csv")

save_users_to_csv() # Main execution
save_repositories_to_csv()
