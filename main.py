import json
import time
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Load configuration from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Function to send email notifications
def send_email(subject, body, email_config):
    msg = MIMEMultipart()
    msg['From'] = email_config['from_email']
    msg['To'] = email_config['to_email']
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
    server.starttls()
    server.login(email_config['from_email'], email_config['password'])
    server.sendmail(email_config['from_email'], email_config['to_email'], msg.as_string())
    server.quit()

# Function to login to a website
def login_realestate_site(driver, login_url, username, password):
    driver.get(login_url)
    time.sleep(3)
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(5)

# Function to scrape listings from a website using Selenium
def scrape_listings_selenium(driver, url, next_button_text):
    listings = []
    driver.get(url)
    time.sleep(5)
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for listing in soup.find_all('div', class_='listing'):
            price = listing.find('span', class_='price').text
            location = listing.find('span', class_='location').text
            bedrooms = listing.find('span', class_='bedrooms').text
            bathrooms = listing.find('span', class_='bathrooms').text
            sqft = listing.find('span', class_='sqft').text
            listings.append({
                'Price': price,
                'Location': location,
                'Bedrooms': bedrooms,
                'Bathrooms': bathrooms,
                'Square Footage': sqft
            })
        try:
            next_button = driver.find_element(By.LINK_TEXT, next_button_text)
            next_button.click()
            time.sleep(5)
        except:
            break
    return pd.DataFrame(listings)

# Main execution
def main():
    driver = webdriver.Chrome()
    all_listings = []

    for site in config['websites']:
        login_realestate_site(driver, site['login_url'], site['username'], site['password'])
        df_site = scrape_listings_selenium(driver, site['url'], site['next_button_text'])
        all_listings.append(df_site)

    driver.quit()

    if all_listings:
        df_all = pd.concat(all_listings, ignore_index=True)
        df_all.to_csv('listings.csv', index=False)

        # Perform data analysis (example: group by location and calculate average price)
        avg_price_by_location = df_all.groupby('Location')['Price'].mean().reset_index()
        avg_price_by_location.columns = ['Location', 'Average Price']

        # Merge average price with new listings
        new_listings = df_all.merge(avg_price_by_location, on='Location')

        # Send email with the new listings and average price by location
        if not new_listings.empty:
            body = new_listings.to_string()
            send_email('New Real Estate Listings with Average Price by Location', body, config['email'])


if __name__ == "__main__":
    main()
