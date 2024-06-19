# Real-Estate-Data-Scraper-and-analyser

# Overview
This project automates the process of scraping real estate listings from multiple websites, analyzing the data, and sending email notifications for new listings. It integrates Selenium for web automation and BeautifulSoup for data extraction. The configuration details, including website URLs and email settings, are stored in a JSON file for easy management.

# Prerequisites
- Python environment with selenium, beautifulsoup4, pandas, and smtplib packages installed.
- ChromeDriver installed and added to your PATH.
- JSON configuration file with website details and email settings.

# Architecture
**Configuration** : A JSON file stores the list of websites to scrape, login credentials, and email settings.
**Web Automation with Selenium**: Automates logging into real estate websites and navigating through listings.
**Data Extraction with BeautifulSoup**: Scrapes property details from the web pages.
**Data Storage and Analysis**: Saves the scraped data in a CSV file and performs basic analysis using Pandas.
**Email Notifications**: Sends an email summary of new listings based on user-defined criteria.

# Running the Project
**Configuration**: Set up the config.json file with the necessary details.
**Execution**: Run the main script main.py, which performs the following:
- Logs into each website specified in the configuration.
- Scrapes property listings using Selenium and BeautifulSoup.
- Aggregates the data into a CSV file.
- Analyzes the data to calculate trends and statistics.
- Sends an email notification with the new listings.
