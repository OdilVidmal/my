import requests
import schedule
import time
from datetime import datetime
import os

# Replace these with your actual login details and the URLs
login_url = 'https://www.sm48.lk/login'
target_url = 'https://www.sm48.lk/viewModule/18'
username = '200635201049'
password = 'thulina@@1234T'

def download_website_source():
    with requests.Session() as session:
        try:
            print("Attempting to access the target page directly...")
            # Try to access the target page directly
            target_response = session.get(target_url, timeout=10)
            print(f"Direct access response status: {target_response.status_code}")
            
            if target_response.status_code == 200 and 'login' not in target_response.url:
                print("Accessed target page directly")
                save_source_code(target_response.text)
            else:
                print("Direct access failed, attempting to log in...")
                # Step 1: Log in
                login_payload = {
                    'username': username,
                    'password': password
                }
                login_response = session.post(login_url, data=login_payload, timeout=10)
                print(f"Login response status: {login_response.status_code}")
                
                # Check if login was successful
                if login_response.status_code == 200:
                    print("Logged in successfully")
                    
                    # Step 2: Access the target page
                    target_response = session.get(target_url, timeout=10)
                    print(f"Target page access response status: {target_response.status_code}")
                    
                    if target_response.status_code == 200:
                        save_source_code(target_response.text)
                    else:
                        print(f"Failed to access the target page. Status code: {target_response.status_code}")
                else:
                    print(f"Failed to log in. Status code: {login_response.status_code}")
        except requests.RequestException as e:
            print(f"An error occurred: {e}")

def save_source_code(source_code):
    file_path = os.path.join(os.path.dirname(__file__), 'index.html')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(source_code)
    print(f"Source code saved to {file_path}")

# Schedule the task to run every 2 days
schedule.every(2).days.do(download_website_source)

# Uncomment the line below to run the function manually for testing
download_website_source()

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
