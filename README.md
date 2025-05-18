## 🗳️ Polymarket US Elections Scraper

This project is a bot designed to scrape live market data from [Polymarket](https://polymarket.com/elections) for the 2024 U.S. Presidential Election. It navigates state and district prediction pages, extracting Republican and Democratic odds, and exports the data to a timestamped CSV file. The goal is to track market sentiment in real time across all states and key congressional districts.

---

### 📦 Features

* Automatically scrapes all U.S. states from the Polymarket election map.
* Includes Maine and Nebraska congressional districts (which split electoral votes).
* Extracts Republican and Democratic market odds.
* Handles dynamic content loading (e.g., hidden prices).
* Saves the results to a structured CSV file with timestamps.
* Uses Selenium with headless Chrome for automated browsing.

---

### ✅ Requirements

* Python 3.8+
* Google Chrome
* Chromedriver (compatible with your Chrome version)

#### Python Libraries

Install the required libraries using:

```bash
pip install selenium beautifulsoup4 pandas lxml
```

---

### ⚙️ Setup

1. **Clone the repository:**

```bash
git clone https://github.com/R4INYIS/polymarket-election-scraper/
cd polymarket-election-scraper
```

2. **Ensure Chromedriver is installed and available in your system PATH.**

You can download it from:
[https://sites.google.com/chromium.org/driver/](https://sites.google.com/chromium.org/driver/)

---

### ▶️ How to Run

To start the scraper, run:

```bash
python main.py
```

The script will:

* Open a headless Chrome browser
* Scrape all state and district election prediction pages
* Extract and organize vote percentages
* Save the results to `polymarket_elections_YYYY-MM-DD_HH-MM.csv`

---

### 📝 Notes

* Script uses off-screen Chrome windows to avoid disrupting your workspace.
* Handles hidden content using dynamic interaction.
* Built for research and educational purposes—please respect Polymarket’s terms of service.
* Can be extended for real-time monitoring, alerts, or visualizations.
