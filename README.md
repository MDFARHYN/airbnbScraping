# 🏠 Airbnb Scraper with Selenium & Regex

**Effortlessly scrape property listings and details from Airbnb** using Selenium, Selenium Stealth, and regular expressions. This tool supports pagination and detailed page scraping for comprehensive data collection.

---

## 🚀 Features

- **Pagination Support**: Automatically navigates through multiple pages to retrieve listings.
- **Selenium Stealth**: Bypass bot detection for uninterrupted scraping.
- **Regex for URL Extraction**: Efficiently captures property URLs and extracts data.
- **Detailed Data Collection**: Retrieves key information such as title, price, address, guest count, bed/bath details, reviews, and host info.
- **CSV Export**: Save data conveniently to a CSV file for further analysis.

---

## 🛠️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/airbnb-scraper.git
   cd airbnb-scraper
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 📖 Usage

1. Open `airbnb_scraper.py` and configure the target URL and number of pages to scrape.
2. Run the scraper:
   ```bash
   python airbnb_scraper.py
   ```
3. Data will be saved to `airbnb_data.csv` in the project directory.

---

## 📄 Code Highlights

- **Pagination**: Automates page-by-page scraping with `go_to_next_page()` to handle the "Next" button.
- **Data Extraction**: Uses regex patterns within `scrape_details_page()` to extract property details such as titles, prices, and more.

---

## 📺 Tutorials and Blog

- [📹 YouTube Tutorial](https://youtube.com) - Watch how to set up and use this scraper.
- [📝 Blog Post](https://yourblog.com) - Step-by-step guide to build and customize the scraper.

---

## ⚠️ Disclaimer

This scraper is for educational purposes only. Please ensure compliance with Airbnb's Terms of Service before using this tool.

---

**Happy Scraping! 🚀**
